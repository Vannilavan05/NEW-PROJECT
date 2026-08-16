import React from "react";
import Navbar from "../components/Navbar";
import HeroSection from "../components/HeroSection";
import Features from "../components/Features";
import Footer from "../components/Footer";

export default function LandingPage({ isDarkMode, toggleTheme }) {
    return (
        <div className="landing-page">
            <Navbar isDarkMode={isDarkMode} toggleTheme={toggleTheme} />
            <main>
                <HeroSection />
                <Features />
                {/* 
        Future Sections:
        <Testimonials /> 
        <CallToAction />
      */}
            </main>
            <Footer />
        </div>
    );
}
