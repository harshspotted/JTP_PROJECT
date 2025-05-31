import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/sonner";
import Image from "next/image";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Project Recommendation WebApp",
  description: "A web application to recommend projects based on employee's skillset.",
  icons: [{ rel: "icon", url: "/jtp_logo.png" }],

};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {/* JTP Logo and text */}
        <div className="flex flex-row items-center p-6">
          <Image src="/jtp_logo.png" alt="JTP Logo" width={50} height={100} />
          <h1 className="text-2xl font-bold ml-4 text-primary">Project Recommendation WebApp</h1>
        </div>
        {/* Border below logo */}
        <div className="border-b border-gray-300"></div>
        {children}
        <Toaster/>
      </body>
    </html>
  );
}
