import { ArrowLeftIcon } from '@heroicons/react/16/solid';
import { useState } from 'react';
import ButtonComponent from './components/Button';
import Card from './components/Card';
import Form, { FormValue } from './components/Form';
import { PredictPayload, PredictorService } from './services/predictor.service';
import { TAXI_ZONES } from './taxi-zones';
import { formatDate } from './utils/format-date';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [hasError, setHasError] = useState(false);
  const [prediction, setPrediction] = useState<{ amount: string; duration: string } | undefined>();

  const onSend = async (formValue: FormValue) => {
    setIsLoading(true);

    const payload: PredictPayload = {
      pickUpDateTime: formatDate(formValue.pickUpDateTime),
      dropOffId: formValue.dropOffId,
      passengersNumber: formValue.passengersNumber,
      pickUpId: formValue.pickUpId,
      paymentMethodId: formValue.isFreeTrip ? 3 : formValue.paymentMethodId,
    };

    try {
      const response = await PredictorService.predict(payload);
      console.log('response', response);

      setIsLoading(false);
      setPrediction(response);
    } catch (error) {
      setHasError(true);
      setIsLoading(false);
      console.error('error', error);
    }
  };

  return (
    <>
      <div className='w-dvw h-dvh bg-gray-900 flex justify-center items-center'>
        <Card>
          {!prediction && !hasError && <Form onSend={onSend} isLoading={isLoading} zones={TAXI_ZONES} />}

          {prediction && !hasError && (
            <>
              <div className='flex '>
                <ButtonComponent
                  onClick={() => {
                    setPrediction(undefined);
                  }}
                  isLoading={isLoading}>
                  <ArrowLeftIcon className='w-4 h-4' />
                  Back
                </ButtonComponent>
              </div>
              <br />

              <span> Price: {prediction.amount} </span>
              <br />
              <br />
              <span> Duration: {prediction.duration} </span>
            </>
          )}

          {hasError && (
            <div>
              <span> An error occurred </span>
              <div className='flex '>
                <ButtonComponent
                  onClick={() => {
                    setHasError(false);
                  }}
                  isLoading={isLoading}>
                  <ArrowLeftIcon className='w-4 h-4' />
                  Back
                </ButtonComponent>
              </div>
            </div>
          )}
        </Card>
      </div>
    </>
  );
}

export default App;
