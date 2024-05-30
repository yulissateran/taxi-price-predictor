export interface PredictPayload {
  pickUpDateTime: string;
  dropOffId: number;
  passengersNumber: number;
  pickUpId: number;
  paymentMethodId: number;
  distanceInMiles: number;
  airportFee: 0 | 1.25;
}

const predict = async (data: PredictPayload): Promise<{ amount: string; duration: string }> => {
  const response = await fetch('http://localhost:5001/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  return await response.json();
};

export const PredictorService = {
  predict,
};
