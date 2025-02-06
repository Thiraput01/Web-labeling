"use client";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  const handleClick = () => {
    router.push("/login");
  };

  return (
    <div className="flex justify-center items-center h-screen flex-col gap-3">
      <h1 className="text-2xl">Welcome to web labeling</h1>
      <button
        onClick={handleClick}
        className=" bg-blue-500 hover:bg-blue-700 text-white py-2 px-4 rounded"
      >
        Go to Login
      </button>
    </div>
  );
}
