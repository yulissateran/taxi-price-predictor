export function getCoordinates(zoneName: string): Promise<{ lat: number; lng: number }> {
  return new Promise((resolve, reject) => {
    try {
      const geocoder = new google.maps.Geocoder();

      geocoder.geocode(
        { address: zoneName, componentRestrictions: { country: 'USA', administrativeArea: 'New York' } },
        (results, status) => {
          if (status === 'OK') {
            if (results?.[0]) {
              const lat = results[0].geometry?.location.lat();
              const lng = results[0].geometry?.location.lng();
              console.log('The locality is ', results[0]);
              resolve({ lat, lng });
            } else {
              reject(new Error('No results found'));
            }
          } else {
            reject(new Error('Geocoder failed due to: ' + status));
          }
        }
      );
    } catch (error) {
      reject(error);
    }
  });
}
