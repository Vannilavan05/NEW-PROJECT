import React from 'react';
import { Moon, Sun, BookOpen } from 'lucide-react';
import './Navbar.css';

export default function Navbar({ isDarkMode, toggleTheme }) {
    return (
        <nav className="navbar glass">
            <div className="container nav-container">

                <div className="nav-logo">
                    <div className="logo-icon bg-gradient shadow-premium">
                        <BookOpen size={22} />
                    </div>
                    <span className="text-gradient logo-text">LearnSpace</span>
                </div>

                <div className="nav-links">
                    <a href="#courses" className="nav-link">Courses</a>
                    <a href="#features" className="nav-link">Features</a>
                    <a href="#about" className="nav-link">About</a>
                </div>

                <div className="nav-actions">
                    <button onClick={toggleTheme} className="theme-toggle hover-lift" aria-label="Toggle Theme">
                        {isDarkMode ? <Sun size={20} /> : <Moon size={20} />}
                    </button>
                    <button className="btn btn-outline hover-lift">Log In</button>
                    <button className="btn btn-primary hover-lift">Start Learning</button>
                </div>
            </div>
        </nav>
    );
}
