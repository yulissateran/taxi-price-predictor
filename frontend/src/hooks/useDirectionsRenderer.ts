import { useMap, useMapsLibrary } from '@vis.gl/react-google-maps';
import { useEffect, useState } from 'react';

let directionsRendererInstance: google.maps.DirectionsRenderer | null = null;

export function useDirectionsRenderer() {
  const map = useMap();
  const routesLibrary = useMapsLibrary('routes');
  const [directionsRenderer, setDirectionsRenderer] = useState<google.maps.DirectionsRenderer | null>();

  useEffect(() => {
    if (!routesLibrary || !map || directionsRendererInstance) {
      setDirectionsRenderer(directionsRendererInstance);
      return;
    }

    directionsRendererInstance = new routesLibrary.DirectionsRenderer({
      map,
    });

    setDirectionsRenderer(directionsRendererInstance);
  }, [routesLibrary, map, directionsRenderer]);

  return directionsRenderer;
}
