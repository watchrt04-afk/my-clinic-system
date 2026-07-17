import streamlit as st
import datetime
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

def get_element_by_month(month):
    if month in [1, 2, 3]: return "ธาตุไฟ"
    elif month in [4, 5, 6]: return "ธาตุลม"
    elif month in [7, 8, 9]: return "ธาตุน้ำ"
    elif month in [10, 11, 12]: return "ธาตุดิน"
    return "ไม่ระบุ"

if 'menu_selection' not in st.session_state:
    st.session_state.menu_selection = "เวชระเบียน"

# Sidebar menu structure
with st.sidebar:
    st.header("🏥 Mor Pat Clinic")
    st.write(f"📅 วันที่: {date.today().strftime('%d/%m/%Y')}")
    st.write("⏰ เวลา: 13:56 น.")
    
    st.subheader("🔹 บริการ")
    if st.button("📁 ข้อมูลร้าน", key="btn_shop", use_container_width=True): st.session_state.menu_selection = "ข้อมูลร้าน"
    
    st.subheader("🔹 คลินิก")
    if st.button("📝 เวชระเบียน (ลงทะเบียน/ค้นหา)", key="btn_reg", use_container_width=True): st.session_state.menu_selection = "เวชระเบียน"
    if st.button("🩺 ห้องตรวจ (วินิจฉัย/รักษา)", key="btn_check", use_container_width=True): st.session_state.menu_selection = "ห้องตรวจ"
    if st.button("💊 ห้องจ่ายยา (คลัง/สั่งยา)", key="btn_pharm", use_container_width=True): st.session_state.menu_selection = "ห้องจ่ายยา"
    if st.button("💰 การเงิน (สรุปบิล/ใบรับรอง)", key="btn_fin", use_container_width=True): st.session_state.menu_selection = "การเงิน"
    
    st.subheader("🔹 หลังบ้านและอื่น ๆ")
    if st.button("🗓️ ตารางนัดหมาย", key="btn_appoint", use_container_width=True): st.session_state.menu_selection = "ตารางนัดหมาย"
    if st.button("📦 สต๊อกยาคงเหลือ", key="btn_stock", use_container_width=True): st.session_state.menu_selection = "สต๊อกยาคงเหลือ"
    if st.button("👨‍⚕️ แพทย์ผู้ตรวจ & ค่าธรรมเนียม", key="btn_docs", use_container_width=True): st.session_state.menu_selection = "แพทย์ผู้ตรวจ"
    if st.button("🏖️ วันลาพนักงาน", key="btn_leaves", use_container_width=True): st.session_state.menu_selection = "วันลาพนักงาน"
    if st.button("📊 รายงาน & ตั้งค่าฟอร์ม", key="btn_reports", use_container_width=True): st.session_state.menu_selection = "รายงาน"

current_patient = next((p for p in st.session_state.patients if p["cn"] == st.session_state.current_patient_cn), st.session_state.patients[0])

# --- เวชระเบียน ---
if st.session_state.menu_selection == "เวชระเบียน":
    st.title("📝 ค้นหาและลงทะเบียนผู้ป่วย (เวชระเบียน)")
    search_query = st.text_input("🔍 ค้นหาผู้ป่วยเดิม (พิมพ์ชื่อ/นามสกุล, CN, เบอร์ติดต่อ, หรือเลขบัตร...)")
    
    found_patients = []
    if search_query:
        found_patients = [p for p in st.session_state.patients if search_query in p["name"] or search_query in p["cn"] or search_query in p["phone"] or search_query in p["id_card"]]
        if found_patients:
            st.success(f"พบข้อมูลผู้ป่วยเดิม {len(found_patients)} รายการ:")
            for fp in found_patients:
                if st.button(f"➔ เปิดเวชระเบียน: {fp['name']} (CN: {fp['cn']})", key=f"sel_{fp['cn']}"):
                    st.session_state.current_patient_cn = fp["cn"]
                    st.session_state.menu_selection = "ห้องตรวจ"
                    st.rerun()
        else:
            st.warning("ไม่พบข้อมูลผู้ป่วยเดิม สามารถกรอกฟอร์มด้านล่างเพื่อเพิ่มข้อมูลผู้ป่วยใหม่ได้ทันที")

    st.markdown("---")
    st.subheader("📋 ฟอร์มข้อมูลเวชระเบียน")
    col1, col2 = st.columns(2)
    with col1:
        is_new = st.checkbox("✨ ติ๊กเพื่อระบุว่าเป็นผู้ป่วยใหม่", value=(len(found_patients) == 0 and search_query != ""))
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
        
        p_age = date.today().year - p_bdate.year
        calculated_element = get_element_by_month(p_bdate.month)
        st.info(f"💡 อายุอัตโนมัติ: {p_age} ปี | ธาตุเจ้าเรือนอัตโนมัติตามเดือนเกิด: {calculated_element}")
        
        p_weight = st.number_input("น้ำหนัก (กก.)", value=60.0 if is_new else current_patient["weight"])
        p_height = st.number_input("ส่วนสูง (ซม.)", value=165.0 if is_new else current_patient["height"])

    with col2:
        p_phone = st.text_input("เบอร์โทรศัพท์ติดต่อ", value="" if is_new else current_patient["phone"])
        p_occup = st.text_input("อาชีพ", value="" if is_new else current_patient["occupation"])
        p_addr = st.text_area("ที่อยู่ปัจจุบัน", value="" if is_new else current_patient["address"])
        p_emerg = st.text_input("เบอร์โทรติดต่อกรณีฉุกเฉิน", value="" if is_new else current_patient["emergency_contact"])
        p_congen = st.text_input("โรคประจำตัว", value="" if is_new else current_patient["congenital_disease"])
        p_allergy = st.text_input("ประวัติการแพ้ยา / แพ้อาหาร", value="" if is_new else current_patient["drug_allergy"])
        p_surg = st.text_input("การผ่าตัด/อุบัติเหตุที่ส่งผลต่อกระดูก", value="" if is_new else current_patient["surgery_history"])
        p_rights = st.selectbox("สิทธิการรักษาพยาบาล", ["ชำระเอง", "เบิกจ่ายราชการ", "บัตรทอง (UC)", "ประกันสังคม"], index=0 if is_new else ["ชำระเอง", "เบิกจ่ายราชการ", "บัตรทอง (UC)", "ประกันสังคม"].index(current_patient["medical_rights"]))

    if st.button("💾 บันทึกข้อมูลและไปยังห้องตรวจ ➔", use_container_width=True):
        new_data = {
            "cn": cn_num, "name": p_name, "id_card": p_id, "birthdate": str(p_bdate), "age": p_age,
            "weight": p_weight, "height": p_height, "phone": p_phone, "occupation": p_occup, "address": p_addr,
            "emergency_contact": p_emerg, "congenital_disease": p_congen, "drug_allergy": p_allergy, "surgery_history": p_surg,
            "ธาตุเจ้าเรือน": calculated_element, "medical_rights": p_rights, "visits": current_patient["visits"] if not is_new else []
        }
        if is_new: st.session_state.patients.append(new_data)
        else:
            for idx, p in enumerate(st.session_state.patients):
                if p["cn"] == cn_num: st.session_state.patients[idx] = new_data
        st.session_state.current_patient_cn = cn_num
        st.session_state.menu_selection = "ห้องตรวจ"
        st.rerun()

# --- ห้องตรวจ ---
elif st.session_state.menu_selection == "ห้องตรวจ":
    st.title("🩺 ห้องตรวจและคัดกรองอาการ")
    
    with st.container(border=True):
        st.subheader(f"👤 ผู้ป่วย: {current_patient['name']} (CN: {current_patient['cn']})")
        st.write(f"**อายุ:** {current_patient['age']} ปี | **ธาตุเจ้าเรือน:** {current_patient['ธาตุเจ้าเรือน']} | **สิทธิ์การรักษา:** {current_patient['medical_rights']}")
        st.write(f"⚠️ **โรคประจำตัว:** {current_patient['congenital_disease']} | **แพ้ยา/อาหาร:** {current_patient['drug_allergy']} | **ประวัติอุบัติเหตุกระดูก:** {current_patient['surgery_history']}")
    
    hist_tab, active_tab = st.tabs(["📜 ประวัติการรักษาย้อนหลัง", "🩺 การตรวจรักษาครั้งนี้"])
    with hist_tab:
        if not current_patient["visits"]:
            st.write("ไม่พบประวัติการรักษาในอดีต")
        for v in current_patient["visits"]:
            with st.expander(f"ครั้งที่ {v['visit_no']} วันที่ {v['date']} วินิจฉัย: {v['dx_thai']}"):
                st.write(f"**CC:** {v['cc']} | **Dx แผนไทย:** {v['dx_thai']} | **หัตถการ:** {v['treatment_plan']} | **ราคา:** {v['price']} บาท")
                
    with active_tab:
        c1, c2, c3 = st.columns(3)
        v_bp = c1.text_input("📊 BP (mmHg)", value=st.session_state.active_visit['bp'])
        v_bt = c2.text_input("🌡️ BT (°C)", value=st.session_state.active_visit['bt'])
        v_pr = c3.text_input("🫀 PR (/min)", value=st.session_state.active_visit['pr'])
        v_cc = st.text_area("🔴 อาการสำคัญ (CC)", value=st.session_state.active_visit['cc'])
        v_pi = st.text_area("🟡 ประวัติปัจจุบัน (PI)", value=st.session_state.active_visit['pi'])
        
        st.markdown("---")
        v_dx_thai = st.selectbox("โรคทางการแพทย์แผนไทย", ["โรคลมปลายปัตคาตสัญญาณ 4 หลัง (U57.33)", "โรคลมปลายปัตคาตสัญญาณ 5 หลัง (U57.34)", "โรคลมปลายปัตคาตสัญญาณ 1 หลัง (U57.31)"])
        v_dx_inter = st.selectbox("โรคทางการแพทย์แผนปัจจุบัน (ICD-10)", ["Myofascial Pain Syndrome (M79.1)", "Office Syndrome (M79.8)"])
        
        st.markdown("---")
        st.subheader("🗺️ Pain Scale & กายวิภาคจุดสัญญาณ")
        pain_score = st.slider("ระดับความเจ็บปวด (Pain Scale)", 0, 10, 5)
        note_box = st.text_input("ระบุจุดกดเจ็บและลักษณะคำอธิบายแปรผล", "พบจุดกดเจ็บกลางบ่า")
        
        st.markdown("---")
        v_plan = st.text_input("หัตถการหลัก", "นวดแก้อาการ / ประคบสมุนไพร")
        v_duration = st.number_input("ระยะเวลา (นาที)", value=60)
        v_price = st.number_input("ค่ารักษาหัตถการ (บาท)", value=500)
        v_summary = st.text_area("สรุปผลการรักษาและคำแนะนำ", "หลีกเลี่ยงการยกของหนัก ยืดเหยียดกล้ามเนื้อ")
        v_doc = st.text_input("ลงชื่อแพทย์ผู้รักษา", value="พท.ว.27777 สมชาย ครับผม")
        
        if st.button("💾 บันทึกและไปยังห้องจ่ายยา ➔", use_container_width=True):
            st.session_state.active_visit.update({
                "bp": v_bp, "bt": v_bt, "pr": v_pr, "cc": v_cc, "pi": v_pi,
                "dx_thai": v_dx_thai, "dx_inter": v_dx_inter, "treatment_plan": v_plan,
                "duration": v_duration, "price": v_price, "summary": v_summary, "doctor": v_doc
            })
            st.session_state.menu_selection = "ห้องจ่ายยา"
            st.rerun()

# --- ห้องจ่ายยา ---
elif st.session_state.menu_selection == "ห้องจ่ายยา":
    st.title("💊 ห้องจ่ายยาและตำรับยาสมุนไพร")
    for m in st.session_state.med_stock:
        if m["stock"] <= 100:
            st.error(f"⚠️ ยาใกล้หมดกรุณาเช็คสต๊อกยา!: {m['name']} เหลือเพียง {m['stock']} แคปซูล")

    col_med1, col_med2 = st.columns([1, 2])
    with col_med1:
        st.subheader("💊 คลังยาปัจจุบัน")
        for m in st.session_state.med_stock:
            st.write(f"- **{m['name']}** (เหลือ: {m['stock']}) | ราคา {m['price']} บาท/เม็ด")
    with col_med2:
        selected_med_name = st.selectbox("เลือกยาที่ต้องการจ่าย", [m["name"] for m in st.session_state.med_stock])
        target_med = next(m for m in st.session_state.med_stock if m["name"] == selected_med_name)
        qty = st.number_input("จำนวนแคปซูล", min_value=1, max_value=int(target_med["stock"]), value=30)
        instr = st.text_input("วิธีรับประทาน", "รับประทานครั้งละ 2 แคปซูล วันละ 3 ครั้ง ก่อนอาหาร เช้า/กลางวัน/เย็น")
        
        if st.button("➕ เพิ่มเข้าบิลสั่งยา"):
            st.session_state.current_med_cart.append({"name": target_med["name"], "qty": qty, "instruction": instr, "total_price": qty * target_med["price"]})
            target_med["stock"] -= qty
            st.success("เพิ่มยาสำเร็จ!")
            
    st.markdown("---")
    if st.session_state.current_med_cart:
        st.subheader("🛒 รายการยาที่เลือกจ่าย")
        st.table(pd.DataFrame(st.session_state.current_med_cart))
        
    if st.button("💾 บันทึกและไปยังขั้นตอนการเงิน ➔", use_container_width=True):
        st.session_state.active_visit["meds"] = st.session_state.current_med_cart
        st.session_state.menu_selection = "การเงิน"
        st.rerun()

# --- การเงิน ---
elif st.session_state.menu_selection == "การเงิน":
    st.title("💰 ฝ่ายการเงินและชำระค่ารักษาพยาบาล")
    h_price = st.session_state.active_visit.get("price", 0)
    grand_med_price = sum(m["total_price"] for m in st.session_state.active_visit.get("meds", []))
    total_raw = h_price + grand_med_price
    
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.subheader("📝 รายละเอียดค่าใช้จ่าย")
            st.write(f"- **ค่ารักษาพยาบาล (หัตถการ):** {h_price} บาท")
            st.write(f"- **ค่าตำรับยาสมุนไพร:** {grand_med_price} บาท")
            st.write(f"### ยอดรวมสุทธิ: {total_raw} บาท")
    with col2:
        dep_paid = st.number_input("💰 หักลบค่ามัดจำเดิมที่มี (บาท)", value=0)
        dep_next = st.number_input("🔮 เพิ่มค่ามัดจำล่วงหน้าการนัดครั้งถัดไป (บาท)", value=0)
        final_collect = total_raw - dep_paid + dep_next
        st.subheader(f"💵 ยอดชำระจริง: {final_collect} บาท")

    st.markdown("---")
    c1, c2 = st.columns(2)
    if c1.button("🖨️ ออกบิลเงินสด (รวมหมวดค่ารักษาพยาบาล)", use_container_width=True): st.info("พิมพ์บิลเงินสดสำเร็จ")
    if c2.button("📜 ออกใบรับรองแพทย์แผนไทย", use_container_width=True): st.info("พิมพ์ใบรับรองแพทย์แผนไทยสำเร็จ")
        
    if st.button("🏁 ยืนยันชำระเงินและเสร็จสิ้นกระบวนการทั้งหมด ✔️", use_container_width=True):
        final_visit = st.session_state.active_visit.copy()
        for p in st.session_state.patients:
            if p["cn"] == current_patient["cn"]: p["visits"].append(final_visit)
        st.session_state.current_med_cart = []
        st.session_state.menu_selection = "บันทึกเสร็จสิ้น"
        st.rerun()

elif st.session_state.menu_selection == "บันทึกเสร็จสิ้น":
    st.balloons()
    st.success("✔️ บันทึกการรักษาสำเร็จ! ระบบพร้อมสำหรับรายถัดไป")
    if st.button("กลับสู่หน้าแรก"):
        st.session_state.menu_selection = "เวชระเบียน"
        st.rerun()

# --- เมนูหลังบ้าน ---
elif st.session_state.menu_selection == "ข้อมูลร้าน":
    st.title("📁 ข้อมูลร้านคลินิก")
    st.info("🏠 **Mor Pat Clinic (หมอพัทธ์ คลินิกการแพทย์แผนไทย)**")
elif st.session_state.menu_selection == "ตารางนัดหมาย":
    st.title("🗓️ ตารางนัดหมาย")
    st.date_input("เลือกปฏิทินตรวจเช็กวันนัดหมาย (F/U)")
elif st.session_state.menu_selection == "สต๊อกยาคงเหลือ":
    st.title("📦 สต๊อกยาคงเหลือ")
    st.dataframe(pd.DataFrame(st.session_state.med_stock))
elif st.session_state.menu_selection == "แพทย์ผู้ตรวจ":
    st.title("👨‍⚕️ แพทย์ผู้ตรวจ")
    st.write("🛠️ **รหัสผู้ประกอบวิชาชีพ:** เปลี่ยนแปลงรูปแบบเป็นรหัส **พท.ว.** นำหน้าเลขทะเบียนเรียบร้อย")
elif st.session_state.menu_selection == "วันลาพนักงาน":
    st.title("🏖️ วันลาพนักงาน")
    st.markdown("🔒 **โควตาวันลาพนักงานคงที่ต่อปี:**\n* ลากิจ 6 วัน/ปี\n* ลาป่วย 30 วัน/ปี\n* ลาพักร้อน 6 วัน/ปี")
elif st.session_state.menu_selection == "รายงาน":
    st.title("📊 รายงาน & ตั้งค่าฟอร์ม")
    st.write("ระบบรายงานสถิติคลินิก และแบบฟอร์มใบยินยอม (Consent Form)")
