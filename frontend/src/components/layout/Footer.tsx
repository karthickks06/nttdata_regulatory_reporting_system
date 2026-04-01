export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* About */}
          <div>
            <h3 className="text-lg font-semibold mb-4">About</h3>
            <p className="text-gray-400 text-sm">
              NTT Data Regulatory Reporting System - An AI-powered platform for automated regulatory compliance and reporting.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <a href="/dashboard" className="text-gray-400 hover:text-white text-sm">
                  Dashboard
                </a>
              </li>
              <li>
                <a href="/regulatory-updates" className="text-gray-400 hover:text-white text-sm">
                  Documents
                </a>
              </li>
              <li>
                <a href="/requirements" className="text-gray-400 hover:text-white text-sm">
                  Requirements
                </a>
              </li>
              <li>
                <a href="/reporting" className="text-gray-400 hover:text-white text-sm">
                  Reports
                </a>
              </li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Resources</h3>
            <ul className="space-y-2">
              <li>
                <a href="/docs" className="text-gray-400 hover:text-white text-sm">
                  Documentation
                </a>
              </li>
              <li>
                <a href="/api" className="text-gray-400 hover:text-white text-sm">
                  API Reference
                </a>
              </li>
              <li>
                <a href="/support" className="text-gray-400 hover:text-white text-sm">
                  Support
                </a>
              </li>
              <li>
                <a href="/changelog" className="text-gray-400 hover:text-white text-sm">
                  Changelog
                </a>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Contact</h3>
            <ul className="space-y-2 text-sm text-gray-400">
              <li>Email: support@nttdata.com</li>
              <li>Phone: +1 (555) 123-4567</li>
              <li>Address: 123 Corporate Blvd</li>
              <li>City, State 12345</li>
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-gray-800">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-400 text-sm">
              &copy; {currentYear} NTT Data. All rights reserved.
            </p>
            <div className="flex gap-6 mt-4 md:mt-0">
              <a href="/privacy" className="text-gray-400 hover:text-white text-sm">
                Privacy Policy
              </a>
              <a href="/terms" className="text-gray-400 hover:text-white text-sm">
                Terms of Service
              </a>
              <a href="/cookies" className="text-gray-400 hover:text-white text-sm">
                Cookie Policy
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
