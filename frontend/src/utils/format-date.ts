// Function to pad single digit numbers with a leading zero
const pad = (number: number) => {
  return number < 10 ? '0' + number : number;
};

export const formatDate = (inputDate: string) => {
  const date = new Date(inputDate);

  // Extract date components
  const year = date.getFullYear();
  const month = pad(date.getMonth() + 1); // Months are zero-based in JS
  const day = pad(date.getDate());
  const hours = pad(date.getHours());
  const minutes = pad(date.getMinutes());
  const seconds = pad(date.getSeconds()); // Default to 00 if no seconds in input

  // Construct the output date string in the desired format
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
};
