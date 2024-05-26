import { Map, useMap } from '@vis.gl/react-google-maps';
import { useEffect } from 'react';
import { useDirectionsRenderer } from './hooks/useDirectionsRenderer';

const MapComponent = ({ direction }: { direction: google.maps.DirectionsResult }) => {
  const directionsRenderer = useDirectionsRenderer();
  const map = useMap();

  useEffect(() => {
    if (directionsRenderer) {
      console.log('setting direction', direction, directionsRenderer);
      directionsRenderer.setMap(map);
      directionsRenderer?.setDirections(direction);
    }
  }, [direction, directionsRenderer, map]);

  return (
    <Map
      style={{ width: '100%', height: '100%' }}
      defaultCenter={{ lat: 40.7128, lng: -74.006 }}
      defaultZoom={12}
      gestureHandling={'greedy'}
      disableDefaultUI={true}
    />
  );
};

export default MapComponent;
