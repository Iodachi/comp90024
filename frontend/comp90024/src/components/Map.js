import React, { Component } from 'react';
import { Map, GoogleApiWrapper } from 'google-maps-react';

const mapStyles = {
  width: '100%',
  height: '100%'
};

export class MapContainer extends Component {
  render() {
    return (
      <Map
        google={this.props.google}
        zoom={6}
        style={mapStyles}
        initialCenter={
          {
            lat: -37.801993,
            lng: 144.959087
          }
        }
      />
    );
  }
}

export default GoogleApiWrapper({
    apiKey: 'AIzaSyBs5U6XwYnch30ZxE78uS3MLgpjetbBH5A'
  })(MapContainer);