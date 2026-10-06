import streamlit as st
import pandas as pd
import math
import plotly.express as px

# ตั้งค่าหน้าจอ
st.set_page_config(page_title="Water Supply Audit Risk Tool", layout="wide", page_icon="💧")

# --- ข้อมูลตัวอย่างโครงการ อบต.ไชยราช ---
CHAIYARAT_DATA = {
    "population": 10007,
    "households": 4276,
    "contract_amt": 49988000,
    "delay_days": 7,
    "penalty_rate": 0.25, # 0.25%
    "expenses": 2650658.67,
    "revenue": 1348878.00,
    "water_produced": 192635
}

st.sidebar.title("เมนูการตรวจสอบ 💧")
st.sidebar.markdown("เครื่องมือวิเคราะห์ความเสี่ยงและสนับสนุนการตรวจสอบระบบประปา")
menu = st.sidebar.radio("เลือกโมดูลการทำงาน:", 
    ["📊 Dashboard สรุปความเสี่ยง", 
     "⚖️ คำนวณสมดุลน้ำ (Water Balance)", 
     "👥 คำนวณขนาดตัวอย่าง (Cochran)", 
     "💰 คำนวณสัญญาและการเงิน", 
     "🕳️ บันทึกพิกัดแนวท่อใต้ดิน"]
)

if menu == "📊 Dashboard สรุปความเสี่ยง":
    st.header("ภาพรวมความเสี่ยงโครงการ (Risk Matrix Dashboard)")
    st.markdown("แสดงผลการประเมินความเสี่ยงทั้ง 8 มิติ เพื่อวางแผนและจัดลำดับความสำคัญในการตรวจสอบ")
    
    # ข้อมูลคะแนนความเสี่ยงจำลองตามผลการตรวจสอบ อบต.ไชยราช
    risk_data = pd.DataFrame({
        "มิติความเสี่ยง": [
            "ปริมาณน้ำดิบต้นทุน", "คุณภาพน้ำประปา", "ผลสัมฤทธิ์การให้บริการ", 
            "ระบบควบคุมอัตโนมัติ (นวัตกรรม)", "ความครบถ้วนของอุปกรณ์", 
            "ระยะเวลาส่งมอบงาน", "การควบคุมพัสดุครุภัณฑ์", "ความยั่งยืนทางการเงิน"
        ],
        "คะแนนความเสี่ยง": [85, 90, 75, 80, 60, 40, 70, 95]
    })
    
    risk_data = risk_data.sort_values(by="คะแนนความเสี่ยง", ascending=True)
    
    # สร้างกราฟด้วย Plotly
    fig = px.bar(risk_data, x="คะแนนความเสี่ยง", y="มิติความเสี่ยง", orientation='h',
                 color="คะแนนความเสี่ยง", color_continuous_scale="Reds",
                 title="การจัดลำดับความเสี่ยง (Risk Ranking)")
    fig.update_layout(xaxis=dict(range=[0, 100]))
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("💡 ข้อเสนอแนะ: จากกราฟพบว่า 'ความยั่งยืนทางการเงิน' และ 'คุณภาพน้ำประปา' มีความเสี่ยงสูงสุด ควรจัดลำดับความสำคัญในการเข้าตรวจสอบและติดตาม Action Plan อย่างเร่งด่วน")

elif menu == "⚖️ คำนวณสมดุลน้ำ (Water Balance)":
    st.header("คำนวณสมดุลน้ำ (Water Balance Calculator)")
    st.write("ประเมินความเพียงพอของแหล่งน้ำดิบต้นทุนเทียบกับอัตราการผลิตต่อวัน")
    
    col1, col2 = st.columns(2)
    with col1:
        volume = st.number_input("ปริมาตรแหล่งน้ำดิบต้นทุนคงเหลือ (ลบ.ม.)", value=12500)
    with col2:
        usage = st.number_input("อัตราการผลิตเฉลี่ย (ลบ.ม./วัน)", value=150)
        
    if usage > 0:
        days_left = volume / usage
        st.metric(label="จำนวนวันที่สามารถผลิตน้ำได้ต่อเนื่อง", value=f"{days_left:.1f} วัน")
        
        if days_left < 60:
            st.error(f"⚠️ วิกฤต! ปริมาณน้ำดิบเหลือใช้เพียง {days_left:.1f} วัน (น้อยกว่า 60 วัน) ควรเร่งจัดหาแหล่งน้ำดิบสำรอง")
        elif days_left < 120:
            st.warning(f"⚠️ เฝ้าระวัง: ปริมาณน้ำดิบเหลือใช้ {days_left:.1f} วัน")
        else:
            st.success(f"✅ ปกติ: ปริมาณน้ำดิบเพียงพอ ({days_left:.1f} วัน)")

elif menu == "👥 คำนวณขนาดตัวอย่าง (Cochran)":
    st.header("คำนวณขนาดตัวอย่างแบบชั้นภูมิ (Stratified Sampling)")
    st.write("สูตร Cochran (1977) พร้อมการปรับแก้ด้วย Finite Population Correction")
    
    use_preset = st.checkbox("โหลดข้อมูลประชากร อบต.ไชยราช", value=True)
    
    N = st.number_input("ขนาดประชากร (N)", value=CHAIYARAT_DATA["population"] if use_preset else 10000)
    confidence = st.selectbox("ระดับความเชื่อมั่น", [0.90, 0.95, 0.99], index=1)
    e = st.number_input("ค่าความคลาดเคลื่อนที่ยอมรับได้ (e)", value=0.05, format="%.3f")
    
    Z = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}[confidence]
    p = 0.5
    q = 1 - p
    
    if st.button("คำนวณขนาดตัวอย่าง"):
        # สูตร Cochran
        n0 = ( (Z**2) * p * q ) / (e**2)
        # ปรับแก้ Finite Population
        n = n0 / (1 + ((n0 - 1) / N))
        
        st.success(f"ขนาดตัวอย่างที่เหมาะสมคือ: {math.ceil(n)} ตัวอย่าง")
        st.write(f"*(จากประชากร {N:,} ราย, ระดับความเชื่อมั่น {confidence*100}%, e = {e})*")

elif menu == "💰 คำนวณสัญญาและการเงิน":
    st.header("คำนวณด้านสัญญาและการเงิน (Financial & Contractual)")
    
    tab1, tab2 = st.tabs(["คำนวณค่าปรับและดอกเบี้ย", "วิเคราะห์ต้นทุนกิจการประปา"])
    
    with tab1:
        st.subheader("การประเมินความเสียหายจากการส่งมอบงานล่าช้า")
        contract_amt = st.number_input("วงเงินตามสัญญา (บาท)", value=CHAIYARAT_DATA["contract_amt"])
        penalty_rate = st.number_input("อัตราค่าปรับ (% ต่อวัน)", value=CHAIYARAT_DATA["penalty_rate"])
        delay_days = st.number_input("จำนวนวันส่งมอบล่าช้า (วัน)", value=CHAIYARAT_DATA["delay_days"])
        
        daily_penalty = contract_amt * (penalty_rate / 100)
        total_penalty = daily_penalty * delay_days
        # ดอกเบี้ยสูญเปล่าอ้างอิง MLR เฉลี่ย 1.2% ต่อปี (สมมติฐาน)
        daily_interest = contract_amt * (1.2 / 100 / 365)
        
        st.metric("ค่าปรับรายวัน (บาท/วัน)", f"{daily_penalty:,.2f}")
        st.metric(f"รวมค่าปรับสะสม {delay_days} วัน (บาท)", f"{total_penalty:,.2f}")
        st.metric("ต้นทุนค่าเสียโอกาส/ดอกเบี้ยสูญเปล่า (บาท/วัน)", f"{daily_interest:,.2f}")

    with tab2:
        st.subheader("วิเคราะห์ต้นทุนการผลิตน้ำประปาต่อหน่วย")
        expense = st.number_input("รายจ่ายรวมกิจการประปา (บาท)", value=CHAIYARAT_DATA["expenses"])
        revenue = st.number_input("รายรับรวมกิจการประปา (บาท)", value=CHAIYARAT_DATA["revenue"])
        water_vol = st.number_input("ปริมาณน้ำประปาที่ผลิตและจำหน่ายได้ (ลบ.ม.)", value=CHAIYARAT_DATA["water_produced"])
        
        if water_vol > 0:
            unit_cost = expense / water_vol
            profit = revenue - expense
            
            st.metric("ต้นทุนการผลิตต่อหน่วย (บาท/ลบ.ม.)", f"{unit_cost:,.2f}")
            if profit < 0:
                st.error(f"กิจการประปาขาดทุนสุทธิ: {profit:,.2f} บาท (ไม่เกิดความยั่งยืนทางการเงิน)")
            else:
                st.success(f"กิจการประปามีกำไรสุทธิ: {profit:,.2f} บาท")

elif menu == "🕳️ บันทึกพิกัดแนวท่อใต้ดิน":
    st.header("บันทึกพิกัดแนวท่อใต้ดิน (Underground Pipeline Log)")
    st.write("บันทึกและตรวจสอบโครงสร้างแนวท่อเมนที่ถูกฝังกลบแล้ว (สามารถแก้ไขข้อมูลในตารางได้โดยตรง)")
    
    # ข้อมูลเริ่มต้นจำลอง
    initial_data = pd.DataFrame([
        {"รหัสจุด (STA)": "STA 0+000", "พิกัด GPS": "11.1234, 99.5678", "รายละเอียดบ่อพัก": "บ่อพักเริ่มต้น", "ขนาดท่อ (มม.)": 225, "ระดับความดัน (PN)": "PN10", "ผลตรวจสอบ": "ตรงตามแบบ"},
        {"รหัสจุด (STA)": "STA 1+500", "พิกัด GPS": "11.1245, 99.5689", "รายละเอียดบ่อพัก": "บ่อพัก Air Valve", "ขนาดท่อ (มม.)": 160, "ระดับความดัน (PN)": "PN10", "ผลตรวจสอบ": "ตรงตามแบบ"},
        {"รหัสจุด (STA)": "STA 3+250", "พิกัด GPS": "11.1260, 99.5701", "รายละเอียดบ่อพัก": "บ่อพัก PRV", "ขนาดท่อ (มม.)": 110, "ระดับความดัน (PN)": "PN8", "ผลตรวจสอบ": "ฝาบ่อไม่ตรงสเปก"},
    ])
    
    # ใช้ data_editor เพื่อให้ผู้ตรวจสอบสามารถพิมพ์แก้ กรอกข้อมูล หรือเพิ่มแถวใหม่ได้
    edited_df = st.data_editor(initial_data, num_rows="dynamic", use_container_width=True)
    
    if st.button("💾 บันทึกข้อมูลเข้าฐานข้อมูล (จำลอง)"):
        st.success("บันทึกข้อมูลแนวท่อสำเร็จ! ข้อมูลถูกจัดเก็บพร้อมสำหรับการสุ่มลงพื้นที่เจาะสำรวจ (Test Pit)")

st.sidebar.markdown("---")
st.sidebar.caption("พัฒนาโดย: นายณัฐพงศ์ อาจพันธ์ | สำนักตรวจเงินแผ่นดินจังหวัดประจวบคีรีขันธ์")