import React, { useState, useEffect } from 'react';
import LandingPage from './pages/LandingPage';

function App() {
    const [isDarkMode, setIsDarkMode] = useState(false);

    useEffect(() => {
        // Check local storage or system preference
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const savedTheme = localStorage.getItem('theme');

        if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
            setIsDarkMode(true);
        }
    }, []);

    useEffect(() => {
        if (isDarkMode) {
            document.documentElement.classList.add('dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('theme', 'light');
        }
    }, [isDarkMode]);

    const toggleTheme = () => setIsDarkMode(!isDarkMode);

    return (
        <div className="app-container">
            <LandingPage isDarkMode={isDarkMode} toggleTheme={toggleTheme} />
        </div>
    );
}

export default App;
