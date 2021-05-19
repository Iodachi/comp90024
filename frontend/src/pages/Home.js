import 'mapbox-gl/dist/mapbox-gl.css';
//import melb from "./../melb.geojson"
import vic from "./../vic.geojson"
import heatmap from "./../processed.geojson"
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
        //var hoveredMelbId =  null;
        var hoveredVicId =  null;

        if (this.isCovid){
        map.on('load', function () {
            // map.addSource("melb", {
            //     "type": "geojson",
            //     "data": melb,
            //     'generateId': true 
            // });
            map.addSource("vic", {
                "type": "geojson",
                "data": vic,
                'generateId': true 
            });
             
            // map.addLayer({
            //     "id": "melb-fills",
            //     "type": "fill",
            //     "source": "melb",
            //     "layout": {},
            //     "paint": {
            //     "fill-color": "#627BC1",
            //     "fill-opacity": ["case",
            //     ["boolean", ["feature-state", "hover"], false],
            //         0.5,
            //         0.1
            //     ]
            //     }
            // });
             
            // map.addLayer({
            //     "id": "melb-borders",
            //     "type": "line",
            //     "source": "melb",
            //     "layout": {},
            //     "paint": {
            //     "line-color": "#627BC1",
            //     "line-width": 2
            //     }
            // });
             
            // map.on("mousemove", "melb-fills", function(e) {
            //     console.log(e)
            //     if (e.features.length > 0) {
            //     if (hoveredMelbId) {
            //         map.setFeatureState({source: 'melb', id: hoveredMelbId}, { hover: false});
            //     }
            //     hoveredMelbId = e.features[0].id;
            //     map.setFeatureState({source: 'melb', id: hoveredMelbId}, { hover: true});
            //     }
            // });
             
            // map.on("mouseleave", "melb-fills", function() {
            //     if (hoveredMelbId) {
            //         map.setFeatureState({source: 'melb', id: hoveredMelbId}, { hover: false});
            //     }
            //     hoveredMelbId =  null;
            // });

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
                new mapboxgl.Popup()
                .setLngLat(e.lngLat)
                .setHTML(e.features[0].properties.vic_lga__3.toLowerCase())
                .addTo(map);
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
            'id': 'earthquakes-heat',
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
            'id': 'earthquakes-point',
            'type': 'circle',
            'source': 'earthquakes',
            'minzoom': 7,
            'paint': {
            // Size circle radius by earthquake magnitude and zoom level
            'circle-radius': [
            'interpolate',
            ['linear'],
            ['zoom'],
            7,
            ['interpolate', ['linear'], ['get', 'mag'], 1, 1, 6, 4],
            16,
            ['interpolate', ['linear'], ['get', 'mag'], 1, 5, 6, 50]
            ],
            // Color circle by earthquake magnitude
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