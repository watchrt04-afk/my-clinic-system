import os

# Create the comprehensive Single-File Python Streamlit Web Application based on the user's workflow design specifications.
code_content = """import streamlit as st
import datetime
import json
import pandas as pd
from datetime import date

# Set up Streamlit Page Configuration
st.set_page_config(
    page_title="Mor Pat Clinic - ระบบบริหารจัดการคลินิกการแพทย์แผนไทย",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session States for Database Emulation
if 'patients' not in st.session_state:
    st.session_state.patients = [
        {
            "cn": "690001",
            "name": "นายกอไก่ กุ๊กกุ๊ก",
            "id_card": "1100100200301",
            "birthdate": "2000-01-15",
            "age": 26,
            "weight": 66.0,
            "height": 168.0,
            "phone": "081-234-5678",
            "occupation": "ค้าขาย",
            "address": "123/45 ถ.สุขุมวิท ต.ปากน้ำ อ.เมือง จ.ระยอง",
            "emergency_contact": "089-876-5432 (บิดา)",
            "congenital_disease": "ไม่มี",
            "drug_allergy": "ปฏิเสธการแพ้ยาและอาหาร",
            "surgery_history": "ปฏิเสธประวัติการผ่าตัดและอุบัติเหตุรุนแรงที่ส่งผลต่อกระดูก",
            "ธาตุเจ้าเรือน": "ธาตุไฟ",
            "medical_rights": "ชำระเอง",
            "visits": [
                {
                    "visit_no": 1,
                    "date": "2026-02-10",
                    "time": "10:30",
                    "bp": "120/80", "bt": "36.5", "pr": "72",
                    "cc": "ปวดตึงบ่าทั้งสองข้าง ร้าวขึ้นกกหู",
                    "pi": "เป็นมา 3 วัน นั่งทำงานคอมพิวเตอร์นานต่อเนื่อง",
                    "dx_thai": "โรคลมปลายปัตคาตสัญญาณ 4 หลัง (U57.33)",
                    "dx_inter": "Myofascial Pain Syndrome (M79.1)",
                    "treatment_plan": "นวดบำบัดทางการแพทย์แผนไทย",
                    "duration": 60,
                    "price": 500,
                    "meds": [{"name": "ยาขับลม", "qty": 30, "instruction": "รับประทานครั้งละ 2 แคปซูล วันละ 3 ครั้ง ก่อนอาหาร เช้า/กลางวัน/เย็น", "total_price": 150}],
                    "summary": "หลังการรักษารู้สึกผ่อนคลาย อาการปวดตึงลดลงอย่างชัดเจน",
                    "doctor": "พท.ว.27777 สมชาย ครับผม",
                    "deposit_paid": 0,
                    "deposit_next": 0
                }
            ]
        }
    ]

if 'current_patient_cn' not in st.session_state:
    st.session_state.current_patient_cn = "690001"

if 'med_stock' not in st.session_state:
    st.session_state.med_stock = [
        {"name": "ยาขับลม", "stock": 500, "desc": "ขับลม ช่วยกระจายลม", "price": 5},
        {"name": "ยาตรีผลา", "stock": 350, "desc": "ระบาย ปรับสมดุลลำไส้", "price": 6},
        {"name": "ยาฟ้าทะลายโจร", "stock": 150, "desc": "ลดไข้ แก้เจ็บคอ", "price": 4},
        {"name": "ยาเศียรสมุทร", "stock": 90, "desc": "บรรเทาอาการปวดศีรษะ", "price": 8}
    ]

if 'current_med_cart' not in st.session_state:
    st.session_state.current_med_cart = []

if 'active_visit' not in st.session_state:
    st.session_state.active_visit = {
        "visit_no": 2,
        "date": str(date.today()),
        "time": "13:56",
        "bp": "", "bt": "", "pr": "",
        "cc": "", "pi": "",
        "dx_thai": "", "dx_inter": "",
        "treatment_plan": "",
        "duration": 0,
        "price": 0,
        "meds": [],
        "summary": "",
        "doctor": "พท.ว.27777 สมชาย ครับผม",
        "deposit_paid": 0,
        "deposit_next": 0
    }

# Helper Function: Calculate Elements based on Birth Month
def get_element_by_month(month):
    if month in [1, 2, 3]: return "ธาตุไฟ (ม.ค.-มี.ค.)"
    elif month in [4, 5, 6]: return "ธาตุลม (เม.ย.-มิ.ย.)"
    elif month in [7, 8, 9]: return "ธาตุน้ำ (ก.ค.-ก.ย.)"
    elif month in [10, 11, 12]: return "ธาตุดิน (ต.ค.-ธ.ค.)"
    return "ไม่ระบุ"

# Custom Styling to mimic the exact UI look from the mockup images
st.markdown("""
<style>
    .main-title { font-size: 26px; font-weight: bold; color: #1E293B; margin-bottom: 5px; }
    .clinic-badge { background-color: #E2E8F0; border-radius: 20px; padding: 5px 20px; font-weight: bold; display: inline-block; font-size: 20px; color: #334155; border: 1px solid #CBD5E1; }
    .sidebar-menu-header { font-weight: bold; font-size: 16px; color: #64748B; margin-top: 15px; margin-bottom: 5px; text-transform: uppercase; }
    .info-box { background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 15px; margin-bottom: 15px; }
    .stock-alert { background-color: #FEE2E2; border: 1px solid #EF4444; color: #991B1B; padding: 10px; border-radius: 6px; font-weight: bold; margin-bottom: 15px; }
    .success-badge { background-color: #DCFCE7; border: 1px solid #22C55E; color: #14532D; padding: 20px; border-radius: 10px; text-align: center; font-size: 18px; font-weight: bold; margin: 20px 0px; }
    .pain-scale-container { background-color: #F1F5F9; border-radius: 8px; padding: 15px; margin-top: 10px; }
    .nav-btn { width: 100%; text-align: left; }
</style>
""", unsafe_allow_html=True)

# App Navigation State
if 'menu_selection' not in st.session_state:
    st.session_state.menu_selection = "เวชระเบียน"

# Sidebar Architecture matching User Layout Requirement
with st.sidebar:
    st.markdown('<div class="clinic-badge">Mor Pat Clinic</div>', unsafe_allow_html=True)
    st.write(f"📅 วันที่: {date.today().strftime('%d/%m/%Y')}")
    st.write("⏰ เวลา: 13:56 น.")
    
    st.markdown('<div class="sidebar-menu-header">บริการ</div>', unsafe_allow_html=True)
    if st.button("📁 ข้อมูลร้าน", key="btn_shop", use_container_width=True): st.session_state.menu_selection = "ข้อมูลร้าน"
    
    st.markdown('<div class="sidebar-menu-header">คลินิก</div>', unsafe_allow_html=True)
    if st.button("📝 เวชระเบียน (ลงทะเบียน/ค้นหา)", key="btn_reg", use_container_width=True): st.session_state.menu_selection = "เวชระเบียน"
    if st.button("🩺 ห้องตรวจ (วินิจฉัย/รักษา)", key="btn_check", use_container_width=True): st.session_state.menu_selection = "ห้องตรวจ"
    if st.button("💊 ห้องจ่ายยา (คลัง/สั่งยา)", key="btn_pharm", use_container_width=True): st.session_state.menu_selection = "ห้องจ่ายยา"
    if st.button("💰 การเงิน (สรุปบิล/ใบรับรอง)", key="btn_fin", use_container_width=True): st.session_state.menu_selection = "การเงิน"
    
    st.markdown('<div class="sidebar-menu-header">ระบบหลังบ้านและอื่น ๆ</div>', unsafe_allow_html=True)
    if st.button("🗓️ ตารางนัดหมาย", key="btn_appoint", use_container_width=True): st.session_state.menu_selection = "ตารางนัดหมาย"
    if st.button("📦 สต๊อกยาคงเหลือ", key="btn_stock", use_container_width=True): st.session_state.menu_selection = "สต๊อกยาคงเหลือ"
    if st.button("👨‍⚕️ แพทย์ผู้ตรวจ & ค่าธรรมเนียม", key="btn_docs", use_container_width=True): st.session_state.menu_selection = "แพทย์ผู้ตรวจ"
    if st.button("🏖️ วันลาพนักงาน", key="btn_leaves", use_container_width=True): st.session_state.menu_selection = "วันลาพนักงาน"
    if st.button("📊 รายงาน & ตั้งค่าฟอร์ม", key="btn_reports", use_container_width=True): st.session_state.menu_selection = "รายงาน"

# Active Patient Selection Logic
patient_dict = {p["cn"]: f"{p['name']} (CN: {p['cn']})" for p in st.session_state.patients}
current_patient = next((p for p in st.session_state.patients if p["cn"] == st.session_state.current_patient_cn), st.session_state.patients[0])

# ==============================================================================
# SCREEN 1: เวชระเบียน (Patient Registration and Search)
# ==============================================================================
if st.session_state.menu_selection == "เวชระเบียน":
    st.markdown('<div class="main-title">ค้นหาและลงทะเบียนผู้ป่วย (เวชระเบียน)</div>', unsafe_allow_html=True)
    
    # Search Box with Dynamic Action Button Prompting
    search_query = st.text_input("🔍 ค้นหาผู้ป่วยเดิม (พิมพ์ชื่อ/นามสกุล, CN, เบอร์ติดต่อ, หรือเลขบัตรประชาชน...)")
    
    found_patients = []
    if search_query:
        found_patients = [p for p in st.session_state.patients if search_query in p["name"] or search_query in p["cn"] or search_query in p["phone"] or search_query in p["id_card"]]
        if found_patients:
            st.success(f"พบข้อมูลผู้ป่วยเดิม {len(found_patients)} รายการ กรุณาคลิกเลือกเพื่อเข้าสู่ห้องตรวจ")
            for fp in found_patients:
                if st.button(f"➔ เปิดเวชระเบียนคุณ: {fp['name']} (CN: {fp['cn']})", key=f"sel_{fp['cn']}"):
                    st.session_state.current_patient_cn = fp["cn"]
                    st.session_state.menu_selection = "ห้องตรวจ"
                    st.rerun()
        else:
            st.warning("ไม่พบข้อมูลผู้ป่วยเดิมในระบบ สามารถระบุรายละเอียดด้านล่างเพื่อเพิ่มข้อมูลผู้ป่วยใหม่ได้ทันที")

    st.markdown("---")
    st.subheader("📋 ฟอร์มข้อมูลผู้ป่วย (ผู้ป่วยใหม่/แก้ไขข้อมูลผู้ป่วยเดิม)")
    
    col1, col2 = st.columns(2)
    with col1:
        is_new = st.checkbox("✨ ติ๊กเพื่อระบุว่าเป็นผู้ป่วยใหม่", value=(len(found_patients) == 0 and search_query != ""))
        
        # CN Automatic Generation Rule logic
        current_year_short = str(date.today().year + 543)[-2:]
        if is_new:
            same_year_count = len([p for p in st.session_state.patients if p["cn"].startswith(current_year_short)])
            suggested_cn = f"{current_year_short}{same_year_count + 1:04d}"
        else:
            suggested_cn = current_patient["cn"]
            
        cn_num = st.text_input("เลขรหัสประจำตัวผู้ป่วย (CN) *ยึดตามปีที่มาครั้งแรก*", value=suggested_cn, disabled=not is_new)
        p_name = st.text_input("ชื่อ - นามสกุล", value="" if is_new else current_patient["name"])
        p_id = st.text_input("เลขประจำตัวประชาชน", value="" if is_new else current_patient["id_card"], max_chars=13)
        p_bdate = st.date_input("วัน/เดือน/ปีเกิด", value=date(2000, 1, 1) if is_new else datetime.datetime.strptime(current_patient["birthdate"], "%Y-%m-%d").date())
        
        # Calculate Age and Element Automations
        p_age = date.today().year - p_bdate.year
        calculated_element = get_element_by_month(p_bdate.month)
        
        st.info(f"💡 คำนวณอายุอัตโนมัติ: {p_age} ปี | ธาตุเจ้าเรือนหลักอัตโนมัติ: {calculated_element}")
        
        p_weight = st.number_input("น้ำหนัก (กก.)", value=60.0 if is_new else current_patient["weight"])
        p_height = st.number_input("ส่วนสูง (ซม.)", value=165.0 if is_new else current_patient["height"])

    with col2:
        p_phone = st.text_input("เบอร์โทรศัพท์ติดต่อ", value="" if is_new else current_patient["phone"])
        p_occup = st.text_input("อาชีพ", value="" if is_new else current_patient["occupation"])
        p_addr = st.text_area("ที่อยู่ปัจจุบัน", value="" if is_new else current_patient["address"])
        p_emerg = st.text_input("เบอร์โทรติดต่อกรณีฉุกเฉิน / ความสัมพันธ์", value="" if is_new else current_patient["emergency_contact"])
        p_congen = st.text_input("โรคประจำตัว", value="" if is_new else current_patient["congenital_disease"])
        p_allergy = st.text_input("ประวัติการแพ้ยา / แพ้อาหาร", value="" if is_new else current_patient["drug_allergy"])
        p_surg = st.text_input("การผ่าตัด/อุบัติเหตุที่ส่งผลต่อกระดูก", value="" if is_new else current_patient["surgery_history"])
        p_rights = st.selectbox("สิทธิการรักษาพยาบาล", ["ชำระเอง", "เบิกจ่ายราชการ", "บัตรทอง (UC)", "ประกันสังคม"], index=0 if is_new else ["ชำระเอง", "เบิกจ่ายราชการ", "บัตรทอง (UC)", "ประกันสังคม"].index(current_patient["medical_rights"]))

    if st.button("💾 บันทึกข้อมูลและไปยังห้องตรวจ ➔", use_container_width=True):
        new_data = {
            "cn": cn_num,
            "name": p_name,
            "id_card": p_id,
            "birthdate": str(p_bdate),
            "age": p_age,
            "weight": p_weight,
            "height": p_height,
            "phone": p_phone,
            "occupation": p_occup,
            "address": p_addr,
            "emergency_contact": p_emerg,
            "congenital_disease": p_congen,
            "drug_allergy": p_allergy,
            "surgery_history": p_surg,
            "ธาตุเจ้าเรือน": calculated_element,
            "medical_rights": p_rights,
            "visits": current_patient["visits"] if not is_new else []
        }
        
        if is_new:
            st.session_state.patients.append(new_data)
        else:
            for idx, p in enumerate(st.session_state.patients):
                if p["cn"] == cn_num:
                    st.session_state.patients[idx] = new_data
        
        st.session_state.current_patient_cn = cn_num
        st.session_state.menu_selection = "ห้องตรวจ"
        st.success("บันทึกข้อมูลสำเร็จ! กำลังนำท่านไปห้องตรวจ...")
        st.rerun()

# ==============================================================================
# SCREEN 2: ห้องตรวจ (Examination and Medical Records)
# ==============================================================================
elif st.session_state.menu_selection == "ห้องตรวจ":
    st.markdown('<div class="main-title">🩺 ห้องตรวจและคัดกรองอาการ</div>', unsafe_allow_html=True)
    
    # Selected Patient Master Summary Panel
    st.markdown(f"""
    <div class="info-box">
        <h4 style='margin:0; color:#1E3A8A;'>ผู้ป่วยปัจจุบัน: {current_patient['name']} | อายุ: {current_patient['age']} ปี | รหัส CN: {current_patient['cn']}</h4>
        <p style='margin:5px 0 0 0; font-size:13px;'>
            <b>เลขบัตรประชาชน:</b> {current_patient['id_card']} | <b>วันเกิด:</b> {current_patient['birthdate']} | <b>ธาตุเจ้าเรือน:</b> {current_patient['ธาตุเจ้าเรือน']}<br>
            <b>น้ำหนัก:</b> {current_patient['weight']} กก. | <b>ส่วนสูง:</b> {current_patient['height']} ซม. | <b>โทรศัพท์:</b> {current_patient['phone']} | <b>อาชีพ:</b> {current_patient['occupation']}<br>
            <b>ที่อยู่:</b> {current_patient['address']}<br>
            <span style='color:#DC2626;'><b>โรคประจำตัว:</b> {current_patient['congenital_disease']} | <b>แพ้ยา/อาหาร:</b> {current_patient['drug_allergy']} | <b>อุบัติเหตุ/ผ่าตัดกระดูก:</b> {current_patient['surgery_history']}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Historical Diagnostic Records Split Pane view
    hist_tab, active_tab = st.tabs(["📜 ประวัติการรักษาย้อนหลัง (History)", "🩺 การตรวจรักษาครั้งนี้ (Active Exam)"])
    
    with hist_tab:
        st.subheader("📚 ประวัติการรักษาที่คลินิกในอดีต")
        if not current_patient["visits"]:
            st.write("ไม่พบประวัติการรักษาก่อนหน้า")
        else:
            for v in current_patient["visits"]:
                with st.expander(f"ครั้งที่ {v['visit_no']} วันที่ {v['date']} เวลา {v['time']} น. - วินิจฉัย: {v['dx_thai']}"):
                    st.write(f"**สัญญาณชีพ:** BP: {v['bp']} mmHg, BT: {v['bt']} °C, PR: {v['pr']} /min")
                    st.write(f"**อาการสำคัญ (CC):** {v['cc']}")
                    st.write(f"**ประวัติปัจจุบัน (PI):** {v['pi']}")
                    st.write(f"**การแพทย์แผนไทย (Dx):** {v['dx_thai']}")
                    st.write(f"**การแพทย์แผนปัจจุบัน:** {v['dx_inter']}")
                    st.write(f"**การหัตถการบำบัด:** {v['treatment_plan']} ({v['duration']} นาที) - ราคา {v['price']} บาท")
                    if v.get('meds'):
                        st.write("**ยาสมุนไพรที่ได้รับ:**")
                        for m in v['meds']:
                            st.write(f"- {m['name']} จำนวน {m['qty']} แคปซูล ({m['instruction']})")
                    st.write(f"**สรุปและคำแนะนำ:** {v['summary']}")
                    st.write(f"**ผู้บันทึก:** {v['doctor']}")

    with active_tab:
        st.subheader(f"📝 บันทึกเวชระเบียนการตรวจรักษา ครั้งที่ {st.session_state.active_visit['visit_no']}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            v_bp = st.text_input("📊 ความดันโลหิต (BP mmHg)", value=st.session_state.active_visit['bp'])
        with col2:
            v_bt = st.text_input("🌡️ อุณหภูมิร่างกาย (BT °C)", value=st.session_state.active_visit['bt'])
        with col3:
            v_pr = st.text_input("🫀 อัตราชีพจร (PR /min)", value=st.session_state.active_visit['pr'])
            
        v_cc = st.text_area("🔴 อาการสำคัญ (Chief Complaint - CC)", value=st.session_state.active_visit['cc'])
        v_pi = st.text_area("🟡 ประวัติปัจจุบัน (Present Illness - PI)", value=st.session_state.active_visit['pi'])
        
        st.markdown("---")
        st.subheader("🧬 การวินิจฉัยโรค (Diagnosis)")
        
        # Dual-school search logic mapping requested text styles
        thai_dx_list = [
            "โรคลมปลายปัตคาตสัญญาณ 4 หลัง (U57.33)",
            "โรคลมปลายปัตคาตสัญญาณ 5 หลัง (U57.34)",
            "โรคลมปลายปัตคาตสัญญาณ 1 หลัง (U57.31)",
            "โรคลมปลายปัตคาตสัญญาณ 3 หลัง (U57.32)",
            "โรคสมุฏฐานธาตุพิการ"
        ]
        inter_dx_list = [
            "Myofascial Pain Syndrome - MPS (M79.1)",
            "Office Syndrome (M79.8)",
            "Lumbar Spondylosis (M47.81)"
        ]
        
        v_dx_thai = st.selectbox("โรคทางการแพทย์แผนไทย (ค้นหาวิธีระบุตามรหัสหรือชื่อไทย)", thai_dx_list)
        v_dx_inter = st.selectbox("โรคทางการแพทย์แผนปัจจุบัน (ICD-10)", inter_dx_list)
        
        st.markdown("---")
        st.subheader("🗺️ กายวิภาคจุดสัญญาณและระบบ Pain Scale")
        
        st.info("🎨 ระบบบันทึกจุดกดเจ็บ (Body Mapping Paint Mode Simulation) และระดับคะแนนความเจ็บปวด")
        
        # Interactive Simulated Anatomy Select Box & Canvas Labels
        col_anat1, col_anat2 = st.columns(2)
        with col_anat1:
            st.image("https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?q=80&w=300&auto=format&fit=crop", caption="แบบจำลองกายวิภาคศาสตร์จุดสัญญาณดัดแปลง", width=250)
            st.markdown("""
            **จุดสัญญาณหลักทางการหัตถเวชกรรมไทย:**
            * A1 ใต้ไหปลาร้า | A2 ช่วงอก | A3 ช่วงลิ้นปี่ | A4 ช่วงสะดือ | A5 ช่วงหัวเหน่า
            * B3 ช่วงเอว | B4 ช่วงหัวตะคาก | B5 ช่วงก้น
            """)
        with col_anat2:
            draw_color = st.color_picker("🎨 เลือกสีสัญลักษณ์วาดจุดเจ็บ/ระบายสีแผนผังร่างกาย", "#EF4444")
            note_box = st.text_input("💬 เพิ่มข้อความจำลองลากวางจุดกดเจ็บ เช่น", "พบจุดกดเจ็บกลางบ่าขวา เสียวร้าวขึ้นฐานกะโหลก")
            st.write(f"📍 สัญลักษณ์ที่วางลงบนแผนผัง: **[X สี {draw_color}]** ข้อความ: {note_box}")
            
        st.markdown("**มาตราวัดระดับความเจ็บปวด (Pain Scale)**")
        pain_score = st.slider("ระบุคะแนนความเจ็บปวด (0 = ไม่เจ็บเลย - 10 = ปวดรุนแรงที่สุด)", 0, 10, 5)
        st.caption("📈 ก่อนการรักษา: 0 1 2 3 4 [5] 6 7 8 9 10 ➔ หลังการรักษาจะประเมินอีกครั้งหน้าถัดไป")
        
        st.markdown("---")
        st.subheader("🩺 แผนการรักษาและหัตถการบำบัด")
        v_plan = st.text_input("หัตถการที่ทำหลัก", "นวดแก้อาการ / นวดประคบสมุนไพร")
        v_duration = st.number_input("ระยะเวลารวมทั้งหมด (นาที)", value=60)
        v_price = st.number_input("ค่ารักษาพยาบาลหัตถการ (บาท)", value=500)
        
        st.markdown("---")
        st.subheader("🌿 สรุปคำแนะนำทางการแพทย์")
        v_summary = st.text_area("สรุปผลการรักษาและคำแนะนำผู้ป่วย", value="หลีกเลี่ยงการยกของหนัก ประคบอุ่นบริเวณบ่า 15 นาที และยืดเหยียดกล้ามเนื้อบ่อยๆ")
        v_doc = st.text_input("ลงชื่อแพทย์ผู้ตรวจการรักษา", value="พท.ว.27777 สมชาย ครับผม")
        
        # Temp save state trigger
        if st.button("💾 บันทึกข้อมูลและสไลด์ไปที่ห้องจ่ายยา ➔", use_container_width=True):
            st.session_state.active_visit.update({
                "bp": v_bp, "bt": v_bt, "pr": v_pr,
                "cc": v_cc, "pi": v_pi,
                "dx_thai": v_dx_thai, "dx_inter": v_dx_inter,
                "treatment_plan": v_plan,
                "duration": v_duration,
                "price": v_price,
                "summary": v_summary,
                "doctor": v_doc
            })
            st.session_state.menu_selection = "ห้องจ่ายยา"
            st.success("บันทึกการคัดกรองวินิจฉัยเรียบร้อย กำลังย้ายไปยังส่วนการจ่ายยาสมุนไพร...")
            st.rerun()

# ==============================================================================
# SCREEN 3: ห้องจ่ายยา (Pharmacy Administration & Inventory)
# ==============================================================================
elif st.session_state.menu_selection == "ห้องจ่ายยา":
    st.markdown('<div class="main-title">💊 ห้องจ่ายยาและตำรับยาสมุนไพร</div>', unsafe_allow_html=True)
    
    # Stock Alert Logic check matching rules
    for m in st.session_state.med_stock:
        if m["stock"] <= 100:
            st.markdown(f'<div class="stock-alert">⚠️ ยาใกล้หมดกรุณาเช็คสต๊อกยา!: {m["name"]} เหลือเพียง {m["stock"]} แคปซูล</div>', unsafe_allow_html=True)

    st.subheader("🔍 ค้นหาและจ่ายตำรับยาสมุนไพรให้ผู้ป่วย")
    
    col_med1, col_med2 = st.columns([1, 2])
    
    with col_med1:
        st.markdown("**💊 รายการตำรับยาที่มีในระบบ**")
        for m in st.session_state.med_stock:
            st.markdown(f"""
            <div style='background-color:#F8FAFC; border:1px solid #CBD5E1; padding:10px; border-radius:5px; margin-bottom:8px;'>
                <b>{m['name']}</b> (คงเหลือ: {m['stock']} แคปซูล)<br>
                <small style='color:#475569;'>สรรพคุณ: {m['desc']}</small><br>
                <span style='color:#059669;'>ราคา: {m['price']} บาท/แคปซูล</span>
            </div>
            """, unsafe_allow_html=True)
            
    with col_med2:
        selected_med_name = st.selectbox("เลือกตำรับยาสมุนไพรที่ต้องการจ่าย", [m["name"] for m in st.session_state.med_stock])
        target_med = next(m for m in st.session_state.med_stock if m["name"] == selected_med_name)
        
        st.info(f"선택: {target_med['name']} | สรรพคุณ: {target_med['desc']}")
        
        qty = st.number_input("ระบุจำนวน (เม็ด/แคปซูล)", min_value=1, max_value=int(target_med["stock"]), value=30)
        
        st.markdown("**วิธีรับประทาน:**")
        c1, c2, c3 = st.columns(3)
        with c1:
            dose = st.number_input("รับประทานครั้งละ (เม็ด/แคปซูล)", min_value=1, value=2)
            freq = st.number_input("วันละ (ครั้ง)", min_value=1, value=3)
        with c2:
            timing = st.radio("ช่วงเวลา", ["ก่อนอาหาร", "หลังอาหาร"])
        with c3:
            meals = st.multiselect("มื้อยา", ["เช้า", "กลางวัน", "เย็น", "ก่อนนอน"], default=["เช้า", "กลางวัน", "เย็น"])
            
        med_note = st.text_input("หมายเหตุเพิ่มเติมเกี่ยวกับยา", "")
        
        instruction_str = f"รับประทานครั้งละ {dose} แคปซูล วันละ {freq} ครั้ง {timing} มื้อ { '/'.join(meals) } {med_note}"
        total_med_price = qty * target_med["price"]
        
        if st.button("➕ เพิ่มตำรับยานี้เข้าสู่บิลใบเสร็จ", use_container_width=True):
            st.session_state.current_med_cart.append({
                "name": target_med["name"],
                "qty": qty,
                "instruction": instruction_str,
                "total_price": total_med_price
            })
            # Deduct stock instantly
            target_med["stock"] -= qty
            st.success(f"เพิ่ม {target_med['name']} สำเร็จในรายการ!")

    st.markdown("---")
    st.subheader("🛒 รายการตำรับยาที่เลือกจ่ายครั้งนี้")
    if not st.session_state.current_med_cart:
        st.write("ยังไม่มีการจ่ายยาสำหรับผู้ป่วยรายนี้")
    else:
        cart_df = pd.DataFrame(st.session_state.current_med_cart)
        st.table(cart_df[["name", "qty", "instruction", "total_price"]])
        
        grand_med_total = sum(item["total_price"] for item in st.session_state.current_med_cart)
        st.markdown(f"**รวมทั้งสิ้น:** {len(st.session_state.current_med_cart)} ตำรับยา | **ราคารวมค่ายาทั้งหมด:** {grand_med_total} บาท")

    if st.button("💾 บันทึกข้อมูลคลังยาและไปยังส่วนคิดเงิน ➔", use_container_width=True):
        st.session_state.active_visit["meds"] = st.session_state.current_med_cart
        st.session_state.menu_selection = "การเงิน"
        st.success("บันทึกการจ่ายยาสมุนไพรลงใบเสร็จเรียบร้อยแล้ว")
        st.rerun()

# ==============================================================================
# SCREEN 4: การเงิน (Billing and Certifications)
# ==============================================================================
elif st.session_state.menu_selection == "การเงิน":
    st.markdown('<div class="main-title">💰 ฝ่ายการเงินและชำระค่ารักษาพยาบาล</div>', unsafe_allow_html=True)
    
    st.subheader(f"💵 สรุปค่ารักษาพยาบาล: {current_patient['name']} - CN{current_patient['cn']}")
    
    # Calculations based on business validation guidelines provided
    h_price = st.session_state.active_visit.get("price", 0)
    h_name = st.session_state.active_visit.get("treatment_plan", "ค่ารักษาพยาบาล (หัตถการ)")
    h_time = st.session_state.active_visit.get("duration", 0)
    
    col_bill1, col_bill2 = st.columns(2)
    
    with col_bill1:
        st.markdown("### 📝 รายการเรียกเก็บเงิน")
        st.markdown(f"""
        * **1. รายการหัตถการทางการแพทย์ (ค่ารักษาพยาบาล):**
            * รายละเอียด: {h_name}
            * ระยะเวลา: {h_time} นาที
            * **รวมราคาหัตถการ:** {h_price} บาท
        """)
        
        grand_med_price = 0
        if st.session_state.active_visit.get("meds"):
            st.markdown("* **2. รายการตำรับยาสมุนไพร:**")
            for idx, m in enumerate(st.session_state.active_visit["meds"]):
                st.markdown(f"    * {idx+1}. {m['name']} ({m['qty']} แคปซูล) : **{m['total_price']} บาท**")
                grand_med_price += m['total_price']
        else:
            st.markdown("* **2. รายการตำรับยาสมุนไพร:** ไม่มี")
            
        total_raw = h_price + grand_med_price
        st.markdown(f"### 💳 ยอดรวมทั้งสิ้นสุทธิ: {total_raw} บาท")

    with col_bill2:
        st.markdown("### 🏦 ระบบจัดสรรค่ามัดจำสะสม")
        dep_paid = st.number_input("💰 ชำระค่ามัดจำเดิมหักลบออก (บาท)", value=0)
        dep_next = st.number_input("🔮 วางค่ามัดจำสำหรับการนัดครั้งถัดไปเพิ่ม (บาท)", value=0)
        
        final_collect = total_raw - dep_paid + dep_next
        st.markdown(f"<h2 style='color:#16A34A;'>💵 ยอดที่ต้องชำระจริง: {final_collect} บาท</h2>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📄 พิมพ์เอกสารสิทธิ์การรักษาและใบเสร็จ")
    
    c_btn1, c_btn2, c_btn3 = st.columns(3)
    with c_btn1:
        if st.button("🖨️ ออกบิลเงินสด / ใบเสร็จรับเงิน", use_container_width=True):
            st.info("ระบบจำลองการส่งไฟล์บิลเงินสดเรียบร้อย: ค่าหัตถการทั้งหมดรวมเป็นรายการ 'ค่ารักษาพยาบาล' สอดคล้องตามระเบียบคลินิก")
    with c_btn2:
        if st.button("📜 ออกใบรับรองแพทย์แผนไทย", use_container_width=True):
            st.info(f"ระบบจัดพิมพ์ใบรับรองแพทย์แผนไทยสำเร็จ ควบคุมสิทธิ์การออกโดย: {st.session_state.active_visit['doctor']}")
    with c_btn3:
        p_by = st.text_input("ผู้รับเงินโดย", "เจ้าหน้าที่ฝ่ายการเงินคลินิก")

    if st.button("🏁 ยืนยันชำระเงินและเสร็จสิ้นกระบวนการรักษาทั้งหมด ✔️", use_container_width=True):
        # Push completed record to master database lists
        final_visit = st.session_state.active_visit.copy()
        final_visit["deposit_paid"] = dep_paid
        final_visit["deposit_next"] = dep_next
        final_visit["final_collected"] = final_collect
        
        # Save to database record index safely
        for p in st.session_state.patients:
            if p["cn"] == current_patient["cn"]:
                p["visits"].append(final_visit)
                
        # Flush temporary cart variables
        st.session_state.current_med_cart = []
        # Update sequence count
        st.session_state.active_visit = {
            "visit_no": len(current_patient["visits"]) + 1,
            "date": str(date.today()),
            "time": "13:56",
            "bp": "", "bt": "", "pr": "",
            "cc": "", "pi": "",
            "dx_thai": "", "dx_inter": "",
            "treatment_plan": "",
            "duration": 0,
            "price": 0,
            "meds": [],
            "summary": "",
            "doctor": "พท.ว.27777 สมชาย ครับผม",
            "deposit_paid": 0,
            "deposit_next": 0
        }
        st.session_state.menu_selection = "บันทึกเสร็จสิ้น"
        st.rerun()

# ==============================================================================
# SCREEN 5: บันทึกเสร็จสิ้น (Success Dashboard View)
# ==============================================================================
elif st.session_state.menu_selection == "บันทึกเสร็จสิ้น":
    st.markdown('<div class="success-badge">✔️ บันทึกการรักษาและรับชำระเงินเสร็จสิ้น! พร้อมสำหรับการรักษาครั้งถัดไป</div>', unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1576091160550-2173dba999ef?q=80&w=600&auto=format&fit=crop", width=400)
    
    if st.button("กลับสู่หน้าแรก (ค้นหาผู้ป่วยเวชระเบียน)", use_container_width=True):
        st.session_state.menu_selection = "เวชระเบียน"
        st.rerun()

# ==============================================================================
# SCREENS: ระบบหลังบ้านและอื่นๆ
# ==============================================================================
elif st.session_state.menu_selection == "ข้อมูลร้าน":
    st.markdown("<div class='main-title'>📁 ข้อมูลร้านคลินิก</div>", unsafe_allow_html=True)
    st.info("🏠 **Mor Pat Clinic (หมอพัทธ์ คลินิกการแพทย์แผนไทย)**\n\nเปิดให้บริการคัดกรอง วินิจฉัยโรค และจ่ายสมุนไพรตามระเบียบวิชาชีพ")

elif st.session_state.menu_selection == "ตารางนัดหมาย":
    st.markdown("<div class='main-title'>🗓️ ระบบบริหารจัดการตารางนัดหมายผู้ป่วย</div>", unsafe_allow_html=True)
    st.date_input("เลือกวันที่เพื่อเรียกดูรายการนัดหมาย", date.today())
    st.write("🔄 แสดงข้อมูลปฏิทินแบบเรียลไทม์ (บูรณาการกับปฏิทินเลือกวันรักษาคงค้างระบบหน้า)")

elif st.session_state.menu_selection == "สต๊อกยาคงเหลือ":
    st.markdown("<div class='main-title'>📦 คลังสต๊อกยาสมุนไพรและสารบบควบคุม</div>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(st.session_state.med_stock))

elif st.session_state.menu_selection == "แพทย์ผู้ตรวจ":
    st.markdown("<div class='main-title'>👨‍⚕️ ตั้งค่าแพทย์ผู้ตรวจ & อัตราค่าธรรมเนียมแพทย์</div>", unsafe_allow_html=True)
    st.write("🛠️ **แก้ไขใบอนุญาต:** จากเดิม เลข ว. ได้เปลี่ยนปรับปรุงเป็นรหัส **พท.ว.** เรียบร้อยถูกต้องตามระเบียบวิชาชีพแพทย์แผนไทย (เช่น พท.ว.27777)")
    st.number_input("⚙️ อัตราส่วนแบ่งค่าธรรมเนียมแพทย์ (%)", min_value=0, max_value=100, value=50)

elif st.session_state.menu_selection == "วันลาพนักงาน":
    st.markdown("<div class='main-title'>🏖️ ระบบคำนวณสิทธิ์วันลาพนักงานคลินิกประเมินอัตโนมัติ</div>", unsafe_allow_html=True)
    st.markdown("""
    **🔒 ล็อคโครงสร้างโควตาวันลาสูงสุดต่อปี:**
    * 🛑 **ลากิจ:** สิทธิ์สูงสุด **6 วัน/ปี**
    * 🩺 **ลาป่วย:** สิทธิ์สูงสุด **30 วัน/ปี**
    * ✈️ **ลาพักร้อน:** สิทธิ์สูงสุด **6 วัน/ปี**
    """)
    st.selectbox("เลือกรายชื่อพนักงานเพื่อกรอกใบลา", ["พท.ว.27777 สมชาย ครับผม", "พนักงานเคาน์เตอร์ บอส"])

elif st.session_state.menu_selection == "รายงาน":
    st.markdown("<div class='main-title'>📊 รายงานสถิติและแบบฟอร์มเอกสารทางกฎหมาย</div>", unsafe_allow_html=True)
    st.write("📄 แบบฟอร์มใบยินยอมรับบริการรักษาพยาบาล (Consent Form) และ รายงานสรุปผลประกอบการคลินิก")
"""

with open("clinic_system.py", "w", encoding="utf-8") as f:
    f.write(code_content)

print("SUCCESS: clinic_system.py created successfully.")