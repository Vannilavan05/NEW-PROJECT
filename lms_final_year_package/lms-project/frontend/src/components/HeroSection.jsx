import React from 'react';
import { PlayCircle, ArrowRight } from 'lucide-react';
import './HeroSection.css';

export default function HeroSection() {
    return (
        <section className="hero">
            <div className="hero-background">
                <div className="blob blob-1"></div>
                <div className="blob blob-2"></div>
            </div>

            <div className="container hero-container">
                <div className="hero-content">
                    <div className="badge glass">
                        ✨ Elevate your learning experience
                    </div>
                    <h1 className="hero-title">
                        Unlock Your Potential with <br />
                        <span className="text-gradient">World-Class Education</span>
                    </h1>
                    <p className="hero-description">
                        Join thousands of students and instructors in an immersive learning platform designed to help you master any skill, anywhere, anytime.
                    </p>
                    <div className="hero-actions">
                        <button className="btn btn-primary btn-large hover-lift">
                            Explore Courses <ArrowRight size={20} style={{ marginLeft: '8px' }} />
                        </button>
                        <button className="btn btn-outline btn-large hover-lift play-btn">
                            <PlayCircle size={20} style={{ marginRight: '8px' }} /> See How it Works
                        </button>
                    </div>

                    <div className="hero-stats">
                        <div className="stat">
                            <h3 className="stat-value text-gradient">10k+</h3>
                            <p className="stat-label">Active Students</p>
                        </div>
                        <div className="stat-divider"></div>
                        <div className="stat">
                            <h3 className="stat-value text-gradient">500+</h3>
                            <p className="stat-label">Expert Instructors</p>
                        </div>
                        <div className="stat-divider"></div>
                        <div className="stat">
                            <h3 className="stat-value text-gradient">1M+</h3>
                            <p className="stat-label">Video Lessons</p>
                        </div>
                    </div>
                </div>

                <div className="hero-image-wrapper">
                    <div className="dashboard-mockup shadow-premium glass">
                        {/* Abstract representation of LMS dashboard */}
                        <div className="mockup-header">
                            <div className="mockup-dots">
                                <span></span><span></span><span></span>
                            </div>
                        </div>
                        <div className="mockup-body">
                            <div className="mockup-nav"></div>
                            <div className="mockup-content">
                                <div className="mockup-card video-card">
                                    <div className="play-icon-large">
                                        <PlayCircle size={48} color="white" />
                                    </div>
                                </div>
                                <div className="mockup-grid">
                                    <div className="mockup-card small"></div>
                                    <div className="mockup-card small"></div>
                                </div>
                            </div>
                        </div>

                        {/* Floating element */}
                        <div className="floating-card glass shadow-premium hover-lift">
                            <div className="fc-icon bg-gradient">👨‍🎓</div>
                            <div className="fc-text">
                                <strong>New course enrolled!</strong>
                                <span>Advanced React Patterns</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}
