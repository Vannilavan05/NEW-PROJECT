import os

app_path = r'c:\Users\vanni\Downloads\NEW-PROJECT-main\NEW-PROJECT-main\app.py'

with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

analytics_route = """
@app.route('/hospital/analytics')
@login_required
@role_required('hospital')
def hospital_analytics():
    import pandas as pd
    conn = get_db()
    cursor = conn.cursor()
    
    # Big Data Analytics Simulation using Pandas
    # 1. Fetch all prescriptions to analyze medicine popularity
    cursor.execute("SELECT medicines, created_at FROM prescriptions WHERE hospital_id = %s", (session['id'],))
    prescriptions = cursor.fetchall()
    
    if not prescriptions:
        return render_template('hospital/analytics.html', no_data=True)
        
    df_pres = pd.DataFrame(prescriptions)
    
    # Process unstructured text (medicines) into actionable insights
    # Split multiline text and strip whitespace
    all_meds = []
    for med_text in df_pres['medicines']:
        meds = [m.strip() for m in med_text.split('\\n') if m.strip()]
        all_meds.extend(meds)
        
    df_meds = pd.DataFrame(all_meds, columns=['Medicine'])
    med_counts = df_meds['Medicine'].value_counts().head(5).to_dict()
    
    # 2. Fetch scan data across the network to identify trends (Simulating big data aggregation)
    cursor.execute("SELECT scan_type, COUNT(*) as count FROM scans GROUP BY scan_type")
    scan_trends_raw = cursor.fetchall()
    scan_trends = {s['scan_type']: s['count'] for s in scan_trends_raw}
    
    return render_template('hospital/analytics.html', 
                          med_counts=med_counts,
                          scan_trends=scan_trends,
                          total_prescriptions=len(df_pres))
"""

if "/hospital/analytics" not in content:
    # insert before # RUN APP
    content = content.replace("# ============================================================================\n# RUN APP", analytics_route + "\n# ============================================================================\n# RUN APP")
    
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Analytics added")
