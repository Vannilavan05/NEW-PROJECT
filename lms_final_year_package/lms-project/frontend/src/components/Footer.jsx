import React from 'react';
import { BookOpen, Github, Twitter, Linkedin, Heart } from 'lucide-react';
import './Footer.css';

export default function Footer() {
    return (
        <footer className="footer">
            <div className="container footer-container">

                <div className="footer-brand">
                    <div className="footer-logo">
                        <BookOpen size={24} className="text-gradient" />
                        <span className="text-gradient logo-text">LearnSpace</span>
                    </div>
                    <p className="footer-description">
                        Empowering the next generation of thinkers, creators, and innovators through accessible world-class education.
                    </p>
                    <div className="social-links">
                        <a href="#" className="social-icon hover-lift"><Twitter size={20} /></a>
                        <a href="#" className="social-icon hover-lift"><Github size={20} /></a>
                        <a href="#" className="social-icon hover-lift"><Linkedin size={20} /></a>
                    </div>
                </div>

                <div className="footer-links-group">
                    <div className="footer-column">
                        <h4>Platform</h4>
                        <a href="#">Browse Courses</a>
                        <a href="#">Instructor Portal</a>
                        <a href="#">Pricing</a>
                        <a href="#">Certificates</a>
                    </div>
                    <div className="footer-column">
                        <h4>Resources</h4>
                        <a href="#">Blog</a>
                        <a href="#">Community</a>
                        <a href="#">Help Center</a>
                        <a href="#">API Documentation</a>
                    </div>
                    <div className="footer-column">
                        <h4>Company</h4>
                        <a href="#">About Us</a>
                        <a href="#">Careers</a>
                        <a href="#">Privacy Policy</a>
                        <a href="#">Terms of Service</a>
                    </div>
                </div>

            </div>

            <div className="footer-bottom container">
                <p>&copy; {new Date().getFullYear()} LMS Platform created with <Heart size={14} fill="red" color="red" style={{ display: "inline", margin: "0 4px" }} /> for final year project.</p>
            </div>
        </footer>
    );
}
