import 'mapbox-gl/dist/mapbox-gl.css';
import melb from "./../melb.geojson"
import vic from "./../vic.geojson"
import React from 'react'
import mapboxgl from '!mapbox-gl';// eslint-disable-line import/no-webpack-loader-syntax
import './Mapbox.css'

mapboxgl.accessToken = 'pk.eyJ1IjoiaW9kYWNoaSIsImEiOiJja29zaGNxbXgwMWllMnhxN201ZXJ0Yjl3In0.6UNecHRhTT17I-PaJOfaNg';
export class Mapbox extends React.Component {
    constructor(props) {
        super(props);
        this.mapContainer = React.createRef();
    }
        
    componentDidMount() {
        const map = new mapboxgl.Map({
            container: this.mapContainer.current,
            style: 'mapbox://styles/iodachi/ckosm3m3y2il318mpgeza2axh',
            center: [144.959087, -37.801993],
            zoom: 9,
        });
        var hoveredMelbId =  null;
        var hoveredVicId =  null;

        map.on('load', function () {
            map.addSource("melb", {
                "type": "geojson",
                "data": melb,
                'generateId': true 
            });

            map.addSource("vic", {
                "type": "geojson",
                "data": vic,
                'generateId': true 
            });
             
            map.addLayer({
                "id": "melb-fills",
                "type": "fill",
                "source": "melb",
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
                "id": "melb-borders",
                "type": "line",
                "source": "melb",
                "layout": {},
                "paint": {
                "line-color": "#627BC1",
                "line-width": 2
                }
            });
             
            map.on("mousemove", "melb-fills", function(e) {
                console.log(e)
                if (e.features.length > 0) {
                if (hoveredMelbId) {
                    map.setFeatureState({source: 'melb', id: hoveredMelbId}, { hover: false});
                }
                hoveredMelbId = e.features[0].id;
                map.setFeatureState({source: 'melb', id: hoveredMelbId}, { hover: true});
                }
            });
             
            map.on("mouseleave", "melb-fills", function() {
                if (hoveredMelbId) {
                    map.setFeatureState({source: 'melb', id: hoveredMelbId}, { hover: false});
                }
                hoveredMelbId =  null;
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
                console.log(e)
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
        });
    }
        
    render() {
        return (
        <div>
            <div ref={this.mapContainer} className="map-container" />
        </div>
        );
    }
}
export default Mapbox;