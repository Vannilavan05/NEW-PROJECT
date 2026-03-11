import React from 'react';
import { BookOpen, Video, CheckCircle, UploadCloud, Users, Settings, Award, BarChart3, Shield } from 'lucide-react';
import './Features.css';

const featureGroups = [
    {
        role: "Student Portal",
        description: "Learn without limits with your personalized learning environment.",
        accent: "blue",
        features: [
            { icon: <BookOpen size={24} />, title: "View Courses", desc: "Browse a vast catalog of topics." },
            { icon: <CheckCircle size={24} />, title: "Enroll in Course", desc: "Seamless enrollment process." },
            { icon: <Video size={24} />, title: "Watch Videos", desc: "High quality streaming player." },
            { icon: <Award size={24} />, title: "Submit Assignments", desc: "Upload works and track grades." }
        ]
    },
    {
        role: "Instructor Dashboard",
        description: "Build, share, and monetize your knowledge effectively.",
        accent: "purple",
        features: [
            { icon: <UploadCloud size={24} />, title: "Create Course", desc: "Intuitive drag-and-drop builder." },
            { icon: <CheckCircle size={24} />, title: "Create Quiz", desc: "Test student knowledge live." },
            { icon: <BarChart3 size={24} />, title: "Grade Assignments", desc: "Bulk grading and feedback tools." },
            { icon: <Users size={24} />, title: "View Analytics", desc: "Monitor student progression." }
        ]
    },
    {
        role: "Admin Controls",
        description: "Maintain perfect harmony across the entire LMS platform.",
        accent: "green",
        features: [
            { icon: <Users size={24} />, title: "Manage Users", desc: "Role assignments & access controls." },
            { icon: <Settings size={24} />, title: "Manage Courses", desc: "Oversee site-wide curriculum." },
            { icon: <BarChart3 size={24} />, title: "View Reports", desc: "Comprehensive system metrics." },
            { icon: <Shield size={24} />, title: "System Settings", desc: "Configure platform behaviors." }
        ]
    }
];

export default function Features() {
    return (
        <section id="features" className="features-section">
            <div className="container">
                <div className="features-header text-center">
                    <h2 className="section-title">One Platform, <span className="text-gradient">Three Powerful Modes</span></h2>
                    <p className="section-description">
                        Whether you're learning new skills, teaching hundreds of students, or managing the institution, LearnSpace provides tailored tools just for you.
                    </p>
                </div>

                <div className="features-grid">
                    {featureGroups.map((group, groupIdx) => (
                        <div key={groupIdx} className={`feature-pillar pillar-${group.accent} hover-lift shadow-premium glass`}>
                            <div className="pillar-header">
                                <h3>{group.role}</h3>
                                <p>{group.description}</p>
                            </div>
                            <div className="feature-list">
                                {group.features.map((feat, idx) => (
                                    <div key={idx} className="feature-item hover-lift">
                                        <div className={`feature-icon icon-${group.accent}`}>
                                            {feat.icon}
                                        </div>
                                        <div className="feature-content">
                                            <h4>{feat.title}</h4>
                                            <p>{feat.desc}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
}
