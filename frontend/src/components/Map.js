import React, { Component } from 'react';
import { Map, GoogleApiWrapper, Marker, InfoWindow } from 'google-maps-react';

const mapStyles = [{
  width: '100%',
  height: '100%'
},
    {
      "featureType": "administrative",
      "elementType": "all",
      "stylers": [
          {
              "visibility": "on"
          },
          {
              "weight": "2.19"
          }
      ]
  },
  {
      "featureType": "landscape",
      "elementType": "all",
      "stylers": [
          {
              "color": "#f2e5d4"
          }
      ]
  },
  {
      "featureType": "poi.park",
      "elementType": "geometry",
      "stylers": [
          {
              "color": "#c5dac6"
          }
      ]
  },
  {
      "featureType": "poi.park",
      "elementType": "labels",
      "stylers": [
          {
              "visibility": "on"
          },
          {
              "lightness": 20
          }
      ]
  },
  {
      "featureType": "road",
      "elementType": "all",
      "stylers": [
          {
              "lightness": 20
          }
      ]
  },
  {
      "featureType": "road.highway",
      "elementType": "geometry",
      "stylers": [
          {
              "color": "#c5c6c6"
          }
      ]
  },
  {
      "featureType": "road.arterial",
      "elementType": "geometry",
      "stylers": [
          {
              "color": "#e4d7c6"
          }
      ]
  },
  {
      "featureType": "road.local",
      "elementType": "geometry",
      "stylers": [
          {
              "color": "#fbfaf7"
          }
      ]
  },
  {
      "featureType": "water",
      "elementType": "all",
      "stylers": [
          {
              "visibility": "on"
          },
          {
              "color": "#acbcc9"
          }
      ]
  }
]


export class MapContainer extends Component {

  state = {
    showingInfoWindow: true,
    activeMarker: {},
    selectedPlace: {},
  };

  onMarkerClick = (props, marker, e) =>
    this.setState({
      selectedPlace: props,
      activeMarker: marker,
      showingInfoWindow: true
    });

    onMapClicked = (props) => {
      if (this.state.showingInfoWindow) {
        this.setState({
          showingInfoWindow: false,
          activeMarker: null
        })
      }
    };

  render() {
    // const triangleCoords = [
    //   {lat: 25.774, lng: -80.190},
    //   {lat: 18.466, lng: -66.118},
    //   {lat: 32.321, lng: -64.757},
    //   {lat: 25.774, lng: -80.190}
    // ];

    return (
      <Map
        google={this.props.google}
        onClick={this.onMapClicked}
        zoom={6}
        styles={mapStyles}
        initialCenter={
          {
            lat: -37.801993,
            lng: 144.959087
          }
        }
      >
        <InfoWindow 
          marker={this.state.activeMarker}
          visible={this.state.showingInfoWindow}>
            <div>
              <h4>Twitter</h4>
            </div>
        </InfoWindow>
        {/* <Polygon
          paths={triangleCoords}
          strokeColor="#0000FF"
          strokeOpacity={0.8}
          strokeWeight={2}
          fillColor="#0000FF"
          fillOpacity={0.35} /> */}
        <Marker
        onClick={this.onMarkerClick}
         name={'University of Melbourne'}></Marker>
      </Map>
    );
  }
}

export default GoogleApiWrapper({
    apiKey: 'AIzaSyDLyQLWVoJpRYadYLuIffczAYjmr3CCvo0'
  })(MapContainer);