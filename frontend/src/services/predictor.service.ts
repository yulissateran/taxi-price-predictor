const predict = async (data: { pickupId: number }): Promise<{ fareAmount: string; duration: string }> => {
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
