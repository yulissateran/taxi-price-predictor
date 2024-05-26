import { useMapsLibrary } from '@vis.gl/react-google-maps';
import { useEffect, useState } from 'react';

let directionsServiceInstance: google.maps.DirectionsService | null = null;

export const useDirectionsService = () => {
  const routesLibrary = useMapsLibrary('routes');
  const [directionsService, setDirectionsService] = useState<google.maps.DirectionsService | null>(null);

  useEffect(() => {
    if (!routesLibrary || directionsServiceInstance) {
      setDirectionsService(directionsServiceInstance);
      return;
    }

    const newDirectionsService = new routesLibrary.DirectionsService();
    directionsServiceInstance = newDirectionsService;
    setDirectionsService(newDirectionsService);
  }, [routesLibrary]);

  return directionsService;
};
