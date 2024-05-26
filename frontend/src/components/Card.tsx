const Card = ({ children }: { children: React.ReactNode }) => {
  return <div className='w-full max-w-xl m-4 rounded-xl bg-white/5 p-8  '>{children}</div>;
};

export default Card;
