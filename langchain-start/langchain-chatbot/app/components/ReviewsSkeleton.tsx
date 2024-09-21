export const ReviewsSkeleton = () => {
  return (
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
      {Array.from({ length: 12 }).map((item, index) => (
        <div key={index}>
          <div className="bg-white shadow rounded-lg overflow-hidden">
            <div className="animate-pulse">
              <div className="p-4">
                <div className="h-8 bg-gray-300 rounded w-3/4 mb-2"></div>
                <div className="h-4 bg-gray-300 rounded w-full mb-2"></div>
                <div className="h-4 bg-gray-300 rounded w-5/6 mb-2"></div>
                <div className="h-4 bg-gray-300 rounded w-4/5"></div>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};
