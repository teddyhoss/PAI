import Link from "next/link";

export function Circle() {
  return (
    <div className="fixed bottom-10 right-10">
      <Link href="/chatbot" replace>
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src="https://developer-blogs.nvidia.com/wp-content/uploads/2024/08/llama-sunglasses-meadow.jpg"
          alt="llama"
          className="w-20 h-20 object-cover rounded-full"
        />
      </Link>
    </div>
  );
}
