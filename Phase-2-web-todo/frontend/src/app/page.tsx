import Link from "next/link";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
          <Link href="/" className="text-xl font-bold text-blue-600">
            Todo App
          </Link>
          <div className="flex gap-4">
            <Link
              href="/login"
              className="text-blue-600 hover:text-blue-700 px-4 py-2 rounded hover:bg-blue-50 transition-colors min-h-[36px]"
            >
              Log In
            </Link>
            <Link
              href="/signup"
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors min-h-[36px]"
            >
              Sign Up
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="max-w-4xl mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h1 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-6">
            Stay Organized, Get Things Done
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            A simple yet powerful todo application to help you manage your tasks,
            track your progress, and stay productive.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/signup"
              className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors text-lg min-h-[48px]"
            >
              Get Started Free
            </Link>
            <Link
              href="/login"
              className="border border-blue-600 text-blue-600 px-8 py-3 rounded-lg hover:bg-blue-50 transition-colors text-lg min-h-[48px]"
            >
              Log In
            </Link>
          </div>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-8 mt-16">
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
              <svg
                className="w-6 h-6 text-blue-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <h3 className="text-lg font-semibold mb-2">Simple & Intuitive</h3>
            <p className="text-gray-600">
              Clean, easy-to-use interface that helps you focus on what matters.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
              <svg
                className="w-6 h-6 text-green-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M5 13l4 4L19 7"
                />
              </svg>
            </div>
            <h3 className="text-lg font-semibold mb-2">Track Progress</h3>
            <p className="text-gray-600">
              Mark tasks as complete and see your accomplishments build up.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
              <svg
                className="w-6 h-6 text-purple-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"
                />
              </svg>
            </div>
            <h3 className="text-lg font-semibold mb-2">Works Everywhere</h3>
            <p className="text-gray-600">
              Access your tasks from any device, anywhere, anytime.
            </p>
          </div>
        </div>

        {/* How it works */}
        <div className="mt-16">
          <h2 className="text-2xl font-bold text-center mb-8">
            How It Works
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-600 mb-2">1</div>
              <h3 className="text-lg font-semibold mb-2">Create an Account</h3>
              <p className="text-gray-600">
                Sign up with your email to get started in seconds.
              </p>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-600 mb-2">2</div>
              <h3 className="text-lg font-semibold mb-2">Add Your Tasks</h3>
              <p className="text-gray-600">
                Quickly add tasks with titles and descriptions.
              </p>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-600 mb-2">3</div>
              <h3 className="text-lg font-semibold mb-2">Stay Organized</h3>
              <p className="text-gray-600">
                Track progress, edit, and complete tasks as you go.
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-16 py-8 text-center text-gray-600">
        <p>&copy; 2026 Todo App. All rights reserved.</p>
      </footer>
    </div>
  );
}
