import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Identity Archetype System 2026", page_icon="🧬", layout="wide")

st.title("🧬 Identity Archetype System (Final Master Blueprint 2026)")
st.write("ระบบประเมินมิติประเภทตัวตนเชิงลึก ผ่าน 5 มิติหลัก (Cognitive, Creative, Physical, Social, Emotional)")

# --------------------------------------------------
# 1. ฐานข้อมูล Mythic Essence ตาม Top 2 มิติเด่น
# --------------------------------------------------
MYTHIC_ESSENCES = {
    "CA": {"color": "Deep Indigo & Golden Spark (ครามลึกล้ำ ประกายทอง)", "name": "ละอองเสกมิติ (Aether Materializer)", "desc": "เปลี่ยนภาพฝันและโครงสร้างซับซ้อนในหัว ให้กลายเป็นผลงานที่จับต้องได้จริงบนโลก"},
    "CP": {"color": "Steel Blue & Crimson Flame (ฟ้าเหล็กกล้า ประกายเพลิง)", "name": "เพลิงผ่าปริศนา (Action Alchemist)", "desc": "ทลายความอึมครึมและปัญหาซับซ้อน ด้วยการลงมือแก้หน้างานอย่างแม่นยำ"},
    "CS": {"color": "Royal Purple & Silver Light (ม่วงรอยัล ประกายเงิน)", "name": "วาทศิลป์สะกดจิต (Strategic Enchantment)", "desc": "ร้อยเรียงตรรกะและเหตุผลเป็นคำพูดสะกดใจ พลิกศัตรูเป็นมิตร ชนะทุกการเจรจา"},
    "CE": {"color": "Slate Gray & Crystal Violet (เทาหินชนวน ประกายม่วงผลึก)", "name": "สติปัญญาไร้พ่าย (Mind Fortress)", "desc": "สมองการวิเคราะห์ที่นิ่งสงบดั่งเกราะแก้ว ตัดสินใจเชิงกลยุทธ์ได้ไร้ความตื่นตระหนก"},
    "AC": {"color": "Electric Violet & Platinum Silver (ม่วงสายฟ้า ประกายเงิน)", "name": "เนตรมองอนาคต (Visionary Architect)", "desc": "มองทะลุช่องโหว่ซับซ้อน ร่ายโครงข่ายนวัตกรรมเชื่อมคนและเทคโนโลยีเข้าด้วยกัน"},
    "AP": {"color": "Vibrant Magenta & Obsidian Black (ชมพูสด ประกายดำออบซิเดียน)", "name": "ลีลาศิลป์มีชีวิต (Kinetic Sorcery)", "desc": "ปลดปล่อยพลังสร้างสรรค์จัดจ้าน ผ่านการเคลื่อนไหวร่างกายและดีไซน์"},
    "AS": {"color": "Prismatic Cyan & Starlight Silver (ฟ้าปริซึม ประกายดาว)", "name": "ประกายจุดคลื่นความคิด (Prismatic Spark)", "desc": "จุดไฟไอเดียคิดต่างให้คนอื่นตื่นเต้น เชื่อมโยงผู้คนมาร่วมสร้างค่านิยมใหม่"},
    "AE": {"color": "Sunset Peach & Glowing Lavender (ส้มพีชยามเย็น ประกายลาเวนเดอร์)", "name": "เวทเนรมิตสัมผัส (Sensory Enchantment)", "desc": "ออกแบบบรรยากาศ อีเวนต์ และประสบการณ์ที่ตรึงใจทั้งสายตา ความรู้สึก และจิตวิญญาณ"},
    "PC": {"color": "Copper Red & Steel Blue (แดงทองแดง ประกายฟ้าเหล็ก)", "name": "หัตถ์สลักความจริง (Master Craftsman)", "desc": "เปลี่ยนแบบแปลนหรือภาพมโนในหัว ให้กลายเป็นโปรดักต์หรือสิ่งประดิษฐ์จริงด้วยมือตนเอง"},
    "PA": {"color": "Flame Ruby & Gold Dust (แดงทับทิม ประกายละอองทอง)", "name": "อาณาเขตกุมมิติ (Spatial Domain)", "desc": "คุมจังหวะ ร่างกาย และพื้นที่ได้อย่างไร้ที่ติ ออกแบบฉากต่อสู้ โชว์ หรือกีฬาขั้นสูง"},
    "PS": {"color": "Solar Orange & Turquoise Wave (ส้มสุริยะ ประกายเทอร์ควอยซ์)", "name": "จังหวะเสน่ห์ตรึงใจ (Rhythmic Flow)", "desc": "สะกดสายตาผู้คนด้วยความสดใสและเสน่ห์การเคลื่อนไหว ส่งมอบพลังงานบวกให้ทุกคนรอบข้าง"},
    "PE": {"color": "Iron Gold & Crimson Heart (ทองเหล็กกล้า ประกายหัวใจชาด)", "name": "กายาเหล็กไหลฟื้นจิต (Unbroken Titan)", "desc": "พละกำลังและความอึดทางกายภาพที่ไม่มีวันล้ม ลุกขึ้นสู้ต่อได้ในทุกสมรภูมิ"},
    "SC": {"color": "Topaz Yellow & Deep Sapphire (เหลืองโทแพซ ประกายไพลิน)", "name": "ข่ายสลายข้อขัดแย้ง (Harmony Weaver)", "desc": "อ่านใจทุกฝ่าย สลายความตึงเครียด และสร้างทางออกที่ทำให้ทุกคนได้ประโยชน์ร่วมกัน"},
    "SA": {"color": "Bright Mint & Rose Gold (เขียวมิ้นต์ ประกายโรสโกลด์)", "name": "พฤกษาถักทอความฝัน (Haven Weaver)", "desc": "สร้างสรรค์แบรนด์หรือพื้นที่อบอุ่น ที่จุดประกายและดึงดูดผู้คนให้อยากมาร่วมเติบโต"},
    "SP": {"color": "Warm Coral & Bright Champagne (ส้มอบอุ่น ประกายแชมเปญ)", "name": "ประทาษรวมใจมวลชน (Beacon of Inspiration)", "desc": "เป็นศูนย์รวมจิตใจ จุดไฟในตัวคนรอบข้าง แล้วนำพาผู้คนลุยทำโปรเจกต์ใหญ่ด้วยความสนุก"},
    "SE": {"color": "Emerald Shield & Warm Sun (เกราะมรกต ประกายตะวันอบอุ่น)", "name": "โอสถประสานวิญญาณ (Empathic Sanctuary)", "desc": "พลังแห่งความเข้าอกเข้าใจและจิตวิทยา เป็นที่พึ่งทางใจและเยียวยาผู้คนรอบข้าง"},
    "EC": {"color": "Pure Crystal & Phoenix Rose (ผลึกขาวบริสุทธิ์ ประกายกุหลาบ)", "name": "เกราะแก้วคริสตัลฟื้นจิต (Crystal Phoenix Aura)", "desc": "พลังสติและจิตวิญญาณหยัดยืดที่ไม่เคยสยบต่อความล้มเหลว ลุกขึ้นใหม่ได้เสมอ"},
    "EA": {"color": "Pure Crystal & Phoenix Rose (ผลึกขาวบริสุทธิ์ ประกายกุหลาบ)", "name": "เกราะแก้วคริสตัลฟื้นจิต (Crystal Phoenix Aura)", "desc": "พลังสติและจิตวิญญาณหยัดยืดที่ไม่เคยสยบต่อความล้มเหลว ลุกขึ้นใหม่ได้เสมอ"},
    "EP": {"color": "Pure Crystal & Phoenix Rose (ผลึกขาวบริสุทธิ์ ประกายกุหลาบ)", "name": "เกราะแก้วคริสตัลฟื้นจิต (Crystal Phoenix Aura)", "desc": "พลังสติและจิตวิญญาณหยัดยืดที่ไม่เคยสยบต่อความล้มเหลว ลุกขึ้นใหม่ได้เสมอ"},
    "ES": {"color": "Pure Crystal & Phoenix Rose (ผลึกขาวบริสุทธิ์ ประกายกุหลาบ)", "name": "เกราะแก้วคริสตัลฟื้นจิต (Crystal Phoenix Aura)", "desc": "พลังสติและจิตวิญญาณหยัดยืดที่ไม่เคยสยบต่อความล้มเหลว ลุกขึ้นใหม่ได้เสมอ"}
}

# --------------------------------------------------
# 2. ฟอร์มแบบทดสอบประเมิน 5 มิติ
# --------------------------------------------------
st.subheader("📝 แบบทดสอบประเมินตัวตน (ระบุระดับความสอดคล้อง 1 - 5)")

with st.form("archetype_form"):
    st.markdown("### มิติที่ [C] Cognitive & Logic (ปัญญา / ตรรกะ / การวิเคราะห์)")
    c_score = st.slider("C: คุณชอบวิเคราะห์ระบบซับซ้อน ค้นหาความจริง และใช้เหตุผลเชิงตรรกะ", 1, 10, 5)
    
    st.markdown("### มิติที่ [A] Creative & Visionary (จินตนาการ / ความคิดสร้างสรรค์)")
    a_score = st.slider("A: คุณชอบคิดนอกกรอบ จินตนาการอนาคต และสร้างสรรค์สิ่งใหม่", 1, 10, 5)
    
    st.markdown("### มิติที่ [P] Physical & Kinetic (กายภาพ / การลงมือทำ / ความคล่องตัว)")
    p_score = st.slider("P: คุณชอบลุยทำจริงหน้างาน ใช้ทักษะทางกายภาพ และมีความอึดสูง", 1, 10, 5)
    
    st.markdown("### มิติที่ [S] Social & Adaptability (สังคม / การปรับตัว / มนุษย์สัมพันธ์)")
    s_score = st.slider("S: คุณเก่งเรื่องการเจรจา อ่านบรรยากาศห้อง และเชื่อมโยงผู้คน", 1, 10, 5)
    
    st.markdown("### มิติที่ [E] Emotional Resilience (จิตใจ / ความยืดหยุ่น / การจัดการอารมณ์)")
    e_score = st.slider("E: คุณนิ่งสงบได้ในภาวะวิกฤต และฟื้นตัวจากความล้มเหลวได้อย่างรวดเร็ว", 1, 10, 5)
    
    submitted = st.form_submit_button("ประมวลผลรหัสตัวตน 120 มิติ")

# --------------------------------------------------
# 3. ระบบประมวลผลและแสดงผลลัพธ์
# --------------------------------------------------
if submitted:
    scores = {"C": c_score, "A": a_score, "P": p_score, "S": s_score, "E": e_score}
    
    # เรียงลำดับมิติจากมากไปน้อยเพื่อหา Top 4 และมิติที่ 5
    sorted_dims = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    top_4 = [dim[0] for dim in sorted_dims[:4]]
    code_4d = "".join(top_4)
    
    fifth_dim, fifth_val = sorted_dims[4]
    
    # กำหนด Suffix Modifier
    mean_val = sum(scores.values()) / 5
    if fifth_val >= mean_val + 1.5:
        modifier = f"+{fifth_dim.lower()}"
        mod_desc = "Supercharged Hidden Power (อาวุธลับเสริมทัพโดดเด่น)"
    elif fifth_val <= mean_val - 1.5:
        modifier = f"-{fifth_dim.lower()}"
        mod_desc = "Vulnerable Blind Spot (จุดสลบหรือจุดเสี่ยงที่ต้องระวังระไว)"
    else:
        modifier = ""
        mod_desc = "Balanced Standard (สมดุลมาตรฐาน)"
        
    full_code = f"{code_4d}{modifier}"
    
    # หา Mythic Essence จาก Top 2
    top_2_key = "".join(top_4[:2])
    essence = MYTHIC_ESSENCES.get(top_2_key, {"color": "Prismatic Aura", "name": "Universal Catalyst", "desc": "พลังแห่งการปรับตัวและสร้างสรรค์อย่างไร้ขีดจำกัด"})

    st.success("ประมวลผลสำเร็จ!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### 🏷️ รหัสตัวตนของคุณ: `{full_code}`")
        st.write(f"**Top 4 Lead Family:** `{code_4d}`")
        st.write(f"**Suffix Modifier:** `{modifier if modifier else 'Balanced'}` ({mod_desc})")
        st.markdown(f"**🎨 ธีมสีประจำมิติ:** {essence['color']}")
        st.markdown(f"✨ **ชื่อแก่นพลัง (Mythic Essence):** **{essence['name']}**")
        st.markdown(f"📜 *นิยาม:* {essence['desc']}")

    with col2:
        st.markdown("### 📊 คะแนนรายมิติ (5 มิติหลัก)")
        score_df = pd.DataFrame(list(scores.items()), columns=["Dimension", "Score"]).set_index("Dimension")
        st.bar_chart(score_df)

    st.markdown("---")
    st.markdown("### 💼 แนวทางคลังอาชีพที่เหมาะสม (Career Playgrounds)")
    
    # ตัวอย่างการแนะนำอาชีพตามสายนำ
    lead = top_4[0]
    if lead == "C":
        st.info("🎯 **สายเทคโนโลยี ระบบ และการวิเคราะห์:** AI Systems Architect, Deep-Tech Venture Builder, Strategic Risk Analyst, Smart City Planner")
    elif lead == "A":
        st.info("🎯 **สายครีเอทีฟ นวัตกรรม และสื่อจินตนาการ:** Creative Technologist, Spatial Computing Architect, Disruptive Social Enterprise Founder")
    elif lead == "P":
        st.info("🎯 **สายปฏิบัติการ กีฬา และฮาร์ดแวร์:** Robotics Engineer, Action Choreographer, Elite Sports Performance Coach, Interaction Hardware Developer")
    elif lead == "S":
        st.info("🎯 **สายสังคม ผู้นำ และการขับเคลื่อนคอมมูนิตี้:** Community Resilience Director, Crisis Negotiation Specialist, Chief People & Cultural Officer")
    elif lead == "E":
        st.info("🎯 **สายจิตวิทยา ภาวะวิกฤต และการฟื้นฟูสุขภาวะ:** Humanitarian Mental Health Director, Executive Mindset & Burnout Recovery Coach, Restorative Justice Facilitator")