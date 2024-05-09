const Card = ({ children }: { children: React.ReactNode }) => {
  return <div className='w-full max-w-lg m-4 rounded-xl bg-white/5 p-6 sm:p-10'>{children}</div>;
};

export default Card;
