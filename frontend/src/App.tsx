import { ArrowLeftIcon } from '@heroicons/react/16/solid';
import { APIProvider } from '@vis.gl/react-google-maps';
import { useState } from 'react';
import MapComponent from './Map';
import ButtonComponent from './components/Button';
import Card from './components/Card';
import Form, { FormValue } from './components/Form';
import { Coordinates } from './coordinates';
import { getCoordinates } from './utils/getCoordinates';
import { useDirectionsService } from './hooks/useDirectionsService';
import yellowTaxi from './images/yellow-taxi.png';
import { PredictPayload, PredictorService } from './services/predictor.service';
import { TAXI_ZONES } from './taxi-zones';
import { formatDate } from './utils/format-date';

function Page({ hasMapsAPILoaded }: { hasMapsAPILoaded: boolean }) {
  const [isLoading, setIsLoading] = useState(false);
  const [hasError, setHasError] = useState(false);
  const [prediction, setPrediction] = useState<{ amount: string; duration: string } | undefined>();
  const directionsService = useDirectionsService();
  const [pickup, setPickup] = useState<Coordinates | undefined>();
  const [dropoff, setDropOff] = useState<Coordinates | undefined>();
  const [direction, setDirection] = useState<google.maps.DirectionsResult | undefined>();

  const onSend = async (formValue: FormValue) => {
    setIsLoading(true);

    const selectedPickupTaxiZone = TAXI_ZONES.find((zone) => zone.LocationID === formValue.pickUpId);
    const selectedDropOffTaxiZone = TAXI_ZONES.find((zone) => zone.LocationID === formValue.dropOffId);

    if (!selectedPickupTaxiZone || !selectedDropOffTaxiZone) {
      return;
    }

    const pickup = await getCoordinates(selectedPickupTaxiZone.Zone);
    const dropoff = await getCoordinates(selectedDropOffTaxiZone.Zone);

    setPickup({ ...pickup, label: selectedPickupTaxiZone.Zone });
    setDropOff({ ...dropoff, label: selectedDropOffTaxiZone.Zone });

    const directionResult = await directionsService?.route({
      origin: new google.maps.LatLng(pickup.lat, pickup.lng),
      destination: new google.maps.LatLng(dropoff.lat, dropoff.lng),
      travelMode: google.maps.TravelMode.DRIVING,
      provideRouteAlternatives: true,
    });

    const distanceInMeters = directionResult?.routes[0]?.legs[0]?.distance?.value || 0;
    const distanceInMiles = distanceInMeters * 0.000621371;

    setDirection(directionResult);

    const payload: PredictPayload = {
      pickUpDateTime: formatDate(formValue.pickUpDateTime),
      dropOffId: formValue.dropOffId,
      passengersNumber: formValue.passengersNumber,
      pickUpId: formValue.pickUpId,
      paymentMethodId: formValue.isFreeTrip ? 3 : formValue.paymentMethodId,
      distanceInMiles,
      airportFee: selectedPickupTaxiZone.service_zone === 'Airports' ? 1.25 : 0,
    };

    try {
      const response = await PredictorService.predict(payload);
      setIsLoading(false);
      setPrediction(response);
    } catch (error) {
      setHasError(true);
      setIsLoading(false);
    }
  };

  const goBack = () => {
    setHasError(false);
    setPrediction(undefined);
    setDirection(undefined);
  };

  return (
    <div className='w-dvw min-h-dvh bg-gray-900 flex flex-col justify-center items-center'>
      <Card>
        {!prediction && !hasError && <Form onSend={onSend} isLoading={isLoading} zones={TAXI_ZONES} />}

        {(prediction || hasError) && (
          <>
            <div className='flex '>
              <ButtonComponent onClick={goBack} isLoading={isLoading}>
                <ArrowLeftIcon className='w-4 h-4' />
                Back
              </ButtonComponent>
            </div>
            {!hasError && hasMapsAPILoaded && direction && (
              <div style={{ height: '400px' }} className='mt-6'>
                <MapComponent direction={direction} />
              </div>
            )}
            {!hasError && prediction && (
              <div className='mt-6'>
                <span className='font-bold'>From </span> <span className='text-sm/6 text-white/50'>{pickup?.label}</span>
                <span className='font-bold'> to </span> <span className='text-sm/6 text-white/50'>{dropoff?.label}</span>
                <br />
                <div className='flex gap-12 mt-6'>
                  <div>
                    <img src={yellowTaxi} alt='logo' className='w-auto h-20 ' />
                  </div>
                  <div>
                    <span> USD {prediction.amount} </span>
                    <br />
                    <span> Duration: {prediction.duration} min </span>
                  </div>
                </div>
              </div>
            )}

            {hasError && <div className='py-8 font-bold'> An error occurred, try again later </div>}
          </>
        )}
      </Card>
    </div>
  );
}

function App() {
  const [mapsAPILoaded, setMapsAPILoaded] = useState(false);

  return (
    <>
      <APIProvider
        apiKey='AIzaSyBeVsjaiDKJ3JS7w_8sUrjfKh4xMHDXiik'
        onLoad={() => {
          setMapsAPILoaded(true);
        }}>
        <Page hasMapsAPILoaded={mapsAPILoaded} />
      </APIProvider>
    </>
  );
}

export default App;
