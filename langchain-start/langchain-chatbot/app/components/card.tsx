export default function BackgroundBlogCard(props: { title: string, content: string }) {
  return (
    <article className="max-w-md mx-auto mt-4 shadow-lg border rounded-md duration-300 hover:shadow-sm">
      <div className="pt-3 ml-4 mr-2 mb-3">
        <h3 className="text-xl text-gray-900">
          {props.title}
        </h3>
        <p className="text-gray-400 text-sm mt-1">{props.content}</p>
      </div>
    </article>
  );
}