import 'mapbox-gl/dist/mapbox-gl.css';
//import melb from "./../melb.geojson"
import vic from "./../vic.geojson"
import heatmap from "./../processed.geojson"
import covidCase from './../case.geojson'
import React from 'react'
import mapboxgl from '!mapbox-gl';// eslint-disable-line import/no-webpack-loader-syntax
import './Home.css'

mapboxgl.accessToken = 'pk.eyJ1IjoiaW9kYWNoaSIsImEiOiJja29zaGNxbXgwMWllMnhxN201ZXJ0Yjl3In0.6UNecHRhTT17I-PaJOfaNg';
export class Home extends React.Component {
    constructor(props) {
        super(props);
        this.mapContainer = React.createRef();
    }

    getScenario(nextProps){
        if(this.props.globalStore.scenario !== nextProps)
            this.isCovid = nextProps.globalStore.scenario === "Victoria Covid"
            this.isHeatmap = nextProps.globalStore.scenario === "Tweet Heatmap"
            this.isLanguages = nextProps.globalStore.scenario === "Languages"
    }

    componentDidMount() {
        const map = new mapboxgl.Map({
            container: this.mapContainer.current,
            style: 'mapbox://styles/iodachi/ckosm3m3y2il318mpgeza2axh',
            center: [144.959087, -37.801993],
            zoom: 9,
        });

        map.on('load', function () {
        })
    }

    UNSAFE_componentWillReceiveProps(nextProps){
        this.getScenario(nextProps)
        const map = new mapboxgl.Map({
            container: this.mapContainer.current,
            style: 'mapbox://styles/iodachi/ckosm3m3y2il318mpgeza2axh',
            center: [144.959087, -37.801993],
            zoom: 9,
        });
        var hoveredVicId =  null;

        if (this.isCovid){
        var colors = ['#fed976', '#feb24c', '#fd8d3c', '#fc4e2a', '#e31a1c'];
        map.on('load', function () {  
            // fetch("http://127.0.0.1:8000/api/cases")
            // .then(res => res.json())
            // .then(
            //     (result) => {
            //        this.covidCase = result
            //     },
            //     (error) => {
            //         this.setState({
            //             error
            //         });
            // })

            map.addSource("covid", {
                "type": "geojson",
                "data": covidCase,
                'generateId': true ,
                cluster: true,
                clusterMaxZoom: 14,
                clusterRadius: 50
            });
            
            map.addLayer({
                id: 'clusters',
                type: 'circle',
                source: 'covid',
                filter: ['has', 'point_count'],
                paint: {
                    'circle-color': [
                        'step', ['get', 'point_count'],
                        colors[0],
                        10,
                        colors[1],
                        50,
                        colors[2],
                        100,
                        colors[3],
                        500,
                        colors[4],
                        ],
                    'circle-radius': [
                        'step', ['get', 'point_count'],
                        10,
                        10,
                        20,
                        50,
                        30,
                        100,
                        40
                ]
                }
            });
             
            map.addLayer({
                id: 'cluster-count',
                type: 'symbol',
                source: 'covid',
                filter: ['has', 'point_count'],
                layout: {
                    'text-field': '{point_count_abbreviated}',
                    'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
                    'text-size': 12
                },
                paint: {
                    'text-color': 'white'
                }
             });

             map.addLayer({
                id: 'unclustered-point',
                type: 'circle',
                source: 'covid',
                filter: ['!', ['has', 'point_count']],
                paint: {
                'circle-color': '#11b4da',
                'circle-radius': 4,
                'circle-stroke-width': 1,
                'circle-stroke-color': '#fff'
                }
            });

            // inspect a cluster on click
            map.on('click', 'clusters', function (e) {
                var features = map.queryRenderedFeatures(e.point, {
                    layers: ['clusters']
                });
                var clusterId = features[0].properties.cluster_id;
                map.getSource('covid').getClusterExpansionZoom(
                    clusterId,
                    function (err, zoom) {
                        if (err) return;
                        map.easeTo({
                            center: features[0].geometry.coordinates,
                            zoom: zoom
                        });
                    });
            });

                map.on('mouseenter', 'clusters', function () {
                    map.getCanvas().style.cursor = 'pointer';
                });
                    
                map.on('mouseleave', 'clusters', function () {
                    map.getCanvas().style.cursor = '';
                });
        });
        
    }else if(this.isHeatmap){
        map.on('load', function () {
            // Add a geojson point source.
            // Heatmap layers also work with a vector tile source.
            map.addSource('heatmap', {
            'type': 'geojson',
            'data': heatmap
            });
             
            map.addLayer(
            {
            'id': 'heat',
            'type': 'heatmap',
            'source': 'heatmap',
            'maxzoom': 9,
            'paint': {
            // Increase the heatmap weight based on frequency and property magnitude
            'heatmap-weight': [
            'interpolate',
            ['linear'],
            ['get', 'mag'],
            0,
            0,
            6,
            1
            ],
            // Increase the heatmap color weight weight by zoom level
            // heatmap-intensity is a multiplier on top of heatmap-weight
            'heatmap-intensity': [
            'interpolate',
            ['linear'],
            ['zoom'],
            0,
            1,
            9,
            3
            ],
            // Color ramp for heatmap.  Domain is 0 (low) to 1 (high).
            // Begin color ramp at 0-stop with a 0-transparancy color
            // to create a blur-like effect.
            'heatmap-color': [
            'interpolate',
            ['linear'],
            ['heatmap-density'],
            0,
            'rgba(33,102,172,0)',
            0.2,
            'rgb(103,169,207)',
            0.4,
            'rgb(209,229,240)',
            0.6,
            'rgb(253,219,199)',
            0.8,
            'rgb(239,138,98)',
            1,
            'rgb(178,24,43)'
            ],
            // Adjust the heatmap radius by zoom level
            'heatmap-radius': [
            'interpolate',
            ['linear'],
            ['zoom'],
            0,
            2,
            9,
            20
            ],
            // Transition from heatmap to circle layer by zoom level
            'heatmap-opacity': [
            'interpolate',
            ['linear'],
            ['zoom'],
            7,
            1,
            9,
            0
            ]
            }
            },
            'waterway-label'
            );
             
            map.addLayer(
            {
            'id': 'heat-point',
            'type': 'circle',
            'source': 'heatmap',
            'minzoom': 7,
            'paint': {
            'circle-radius': [
            'interpolate',
            ['linear'],
            ['zoom'],
            7,
            ['interpolate', ['linear'], ['get', 'mag'], 1, 1, 6, 4],
            16,
            ['interpolate', ['linear'], ['get', 'mag'], 1, 5, 6, 50]
            ],

            'circle-color': [
            'interpolate',
            ['linear'],
            ['get', 'mag'],
            1,
            'rgba(33,102,172,0)',
            2,
            'rgb(103,169,207)',
            3,
            'rgb(209,229,240)',
            4,
            'rgb(253,219,199)',
            5,
            'rgb(239,138,98)',
            6,
            'rgb(178,24,43)'
            ],
            'circle-stroke-color': 'white',
            'circle-stroke-width': 1,
            // Transition from heatmap to circle layer by zoom level
            'circle-opacity': [
            'interpolate',
            ['linear'],
            ['zoom'],
            7,
            0,
            8,
            1
            ]
            }
            },
            'waterway-label'
            );
            });
    }else if (this.isLanguages){
            
        map.on('load', function () {  

        fetch("http://127.0.0.1:8000/api/language")
        .then(res => res.json())
        .then(
            (result) => {
                this.languages = result
            },
            (error) => {
                this.setState({
                    error
                });
        })
            map.addSource("vic", {
                "type": "geojson",
                "data": vic,
                'generateId': true 
            });
            map.addLayer({
                "id": "vic-fills",
                "type": "fill",
                "source": "vic",
                "layout": {},
                "paint": {
                "fill-color": "#627BC1",
                "fill-opacity": ["case",
                ["boolean", ["feature-state", "hover"], false],
                    0.5,
                    0.1
                ]
                }
            });
             
            map.addLayer({
                "id": "vic-borders",
                "type": "line",
                "source": "vic",
                "layout": {},
                "paint": {
                "line-color": "#627BC1",
                "line-width": 2
                }
            });
             
            map.on("mousemove", "vic-fills", function(e) {
                if (e.features.length > 0) {
                if (hoveredVicId) {
                    map.setFeatureState({source: 'vic', id: hoveredVicId}, { hover: false});
                }
                hoveredVicId = e.features[0].id;
                map.setFeatureState({source: 'vic', id: hoveredVicId}, { hover: true});
                }
            });
             
            map.on("mouseleave", "vic-fills", function() {
                if (hoveredVicId) {
                    map.setFeatureState({source: 'vic', id: hoveredVicId}, { hover: false});
                }
                hoveredVicId =  null;
            });

            map.on('click', 'vic-fills', function (e) {
                console.log(this.languages)
                new mapboxgl.Popup()
                .setLngLat(e.lngLat)
                .setHTML(JSON.stringify(this.languages[e.features[0].properties.vic_lga__3]))
                .addTo(map);
            });
        });
    }
    }
        
    render() {
        return (
        <div>
            <div ref={this.mapContainer} className="map-container" />
        </div>
        );
    }
}
export default Home;