import streamlit as st
import streamlit.components.v1 as components

# กำหนดค่าหน้าเว็บให้ขยายเต็มหน้าจอ และซ่อน Padding ขอบของ Streamlit
st.set_page_config(
    page_title="Water Supply Audit Risk Tool - สตง.",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ลบ padding ขอบของ Streamlit ออกเพื่อให้ Dashboard สวยงามแบบ Web App เต็มจอ
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }
    </style>
""", unsafe_allow_html=True)

# ฝังระบบ Web Application ฉบับเต็ม (HTML, Tailwind CSS, Chart.js, Lucide Icons)
html_code = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Water Supply Audit Risk Tool - สำนักงานการตรวจเงินแผ่นดิน</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Lucide Icons CDN -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <!-- Google Fonts: Sarabun & Prompt -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@400;500;600;700&family=Sarabun:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Sarabun', 'sans-serif'],
                        heading: ['Prompt', 'sans-serif'],
                    },
                    colors: {
                        audit: {
                            50: '#f0f5fa',
                            100: '#e1ecf5',
                            500: '#1b4d7e',
                            600: '#143b63',
                            700: '#0e2b49',
                            800: '#0a1e33',
                            900: '#061320',
                            gold: '#c59b27'
                        }
                    }
                }
            }
        }
    </script>
    <style>
        @media print {
            body * { visibility: hidden; }
            #printable-area, #printable-area * { visibility: visible; }
            #printable-area { position: absolute; left: 0; top: 0; width: 100%; }
            .no-print { display: none !important; }
        }
        .custom-scrollbar::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background-color: #cbd5e1;
            border-radius: 4px;
        }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 font-sans antialiased min-h-screen flex flex-col">

    <header class="bg-gradient-to-r from-audit-800 via-audit-700 to-audit-600 text-white shadow-lg sticky top-0 z-40">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-20">
                <div class="flex items-center space-x-3">
                    <div class="w-12 h-12 bg-white/10 rounded-xl p-2 border border-audit-gold/30 flex items-center justify-center text-audit-gold shadow-inner">
                        <i data-lucide="shield-alert" class="w-8 h-8"></i>
                    </div>
                    <div>
                        <div class="flex items-center space-x-2">
                            <span class="text-xs uppercase tracking-wider font-semibold bg-audit-gold/20 text-amber-300 px-2 py-0.5 rounded border border-audit-gold/40">สตง. • ชำนาญการพิเศษ</span>
                            <span class="text-xs text-slate-300 font-medium">State Audit Engineering System</span>
                        </div>
                        <h1 class="text-lg md:text-xl font-heading font-bold text-white tracking-tight">Water Supply Audit Risk Tool</h1>
                        <p class="text-xs text-slate-200">เครื่องมือวิเคราะห์ความเสี่ยงและสนับสนุนการตรวจสอบระบบผลิตน้ำประปา</p>
                    </div>
                </div>
                
                <div class="flex items-center space-x-2 sm:space-x-3">
                    <button id="btn-load-sample" onclick="loadSampleData()" class="inline-flex items-center space-x-1.5 px-3.5 py-2 rounded-lg bg-amber-500 hover:bg-amber-600 text-slate-900 font-semibold text-xs md:text-sm shadow-md transition transform active:scale-95">
                        <i data-lucide="database" class="w-4 h-4"></i>
                        <span class="hidden sm:inline">โหลดตัวอย่าง</span> <span>อบต.ไชยราช (๔๙.๙๘ ลบ.)</span>
                    </button>
                    <button onclick="window.print()" class="inline-flex items-center space-x-1.5 px-3.5 py-2 rounded-lg bg-white/10 hover:bg-white/20 text-white text-xs md:text-sm font-medium border border-white/20 transition">
                        <i data-lucide="printer" class="w-4 h-4"></i>
                        <span class="hidden md:inline">พิมพ์กระดาษทำการ</span>
                    </button>
                </div>
            </div>

            <!-- Tab Navigation Menu -->
            <div class="flex space-x-1 overflow-x-auto no-scrollbar border-t border-white/10 text-xs sm:text-sm font-medium py-1.5">
                <button onclick="switchTab('dashboard')" class="tab-btn px-4 py-2 rounded-lg transition whitespace-nowrap flex items-center space-x-1.5 bg-white/20 text-white shadow" data-tab="dashboard">
                    <i data-lucide="layout-dashboard" class="w-4 h-4"></i>
                    <span>แผงแดชบอร์ด 8 มิติ</span>
                </button>
                <button onclick="switchTab('water-balance')" class="tab-btn px-4 py-2 rounded-lg transition whitespace-nowrap flex items-center space-x-1.5 text-slate-200 hover:bg-white/10" data-tab="water-balance">
                    <i data-lucide="droplet" class="w-4 h-4"></i>
                    <span>1. สมดุลน้ำ (Water Balance)</span>
                </button>
                <button onclick="switchTab('sampling')" class="tab-btn px-4 py-2 rounded-lg transition whitespace-nowrap flex items-center space-x-1.5 text-slate-200 hover:bg-white/10" data-tab="sampling">
                    <i data-lucide="users-round" class="w-4 h-4"></i>
                    <span>2. ขนาดตัวอย่าง Cochran</span>
                </button>
                <button onclick="switchTab('financial')" class="tab-btn px-4 py-2 rounded-lg transition whitespace-nowrap flex items-center space-x-1.5 text-slate-200 hover:bg-white/10" data-tab="financial">
                    <i data-lucide="circle-dollar-sign" class="w-4 h-4"></i>
                    <span>3. สัญญา & การเงิน</span>
                </button>
                <button onclick="switchTab('pipeline')" class="tab-btn px-4 py-2 rounded-lg transition whitespace-nowrap flex items-center space-x-1.5 text-slate-200 hover:bg-white/10" data-tab="pipeline">
                    <i data-lucide="map-pin" class="w-4 h-4"></i>
                    <span>4. แนวท่อใต้ดิน 25 กม.</span>
                </button>
                <button onclick="switchTab('checklist')" class="tab-btn px-4 py-2 rounded-lg transition whitespace-nowrap flex items-center space-x-1.5 text-slate-200 hover:bg-white/10" data-tab="checklist">
                    <i data-lucide="check-square" class="w-4 h-4"></i>
                    <span>5. Checklist & Risk Matrix</span>
                </button>
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 w-full" id="printable-area">
        
        <!-- TAB: DASHBOARD -->
        <section id="tab-dashboard" class="tab-content space-y-6">
            <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div class="space-y-1">
                    <div class="flex items-center space-x-2">
                        <span class="px-2.5 py-0.5 text-xs font-semibold rounded bg-blue-100 text-blue-800">โครงการตรวจสอบผลสัมฤทธิ์และประสิทธิภาพ</span>
                        <span id="badge-risk-status" class="px-2.5 py-0.5 text-xs font-bold rounded bg-red-100 text-red-700 animate-pulse">ความเสี่ยงระดับสูงมาก</span>
                    </div>
                    <h2 class="text-xl font-heading font-bold text-slate-800" id="project-title-display">โครงการก่อสร้างระบบผลิตน้ำประปาพร้อมวางท่อเมน ตำบลไชยราช</h2>
                    <p class="text-sm text-slate-500">หน่วยรับตรวจ: <span id="project-auditee-display" class="font-medium text-slate-700">อบต.ไชยราช อ.บางสะพานน้อย จ.ประจวบคีรีขันธ์</span> | วงเงินกู้: <span id="project-budget-display" class="font-medium text-slate-700">49,988,000 บาท</span></p>
                </div>
                <div class="flex flex-wrap items-center gap-3">
                    <div class="bg-slate-50 px-4 py-2 rounded-xl border border-slate-200 text-center">
                        <span class="text-xs text-slate-400 block font-medium">คะแนนความเสี่ยงรวม</span>
                        <span id="total-risk-score" class="text-2xl font-bold font-heading text-red-600">112</span>
                        <span class="text-[10px] text-slate-400">/ 200 คะแนน</span>
                    </div>
                    <div class="bg-slate-50 px-4 py-2 rounded-xl border border-slate-200 text-center">
                        <span class="text-xs text-slate-400 block font-medium">มิติเสี่ยงวิกฤต (&ge;16)</span>
                        <span id="critical-risk-count" class="text-2xl font-bold font-heading text-amber-600">3</span>
                        <span class="text-[10px] text-slate-400">จาก 8 มิติ</span>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm relative overflow-hidden">
                    <div class="absolute -right-2 -bottom-2 text-slate-100 pointer-events-none"><i data-lucide="users" class="w-20 h-20"></i></div>
                    <p class="text-xs font-medium text-slate-500">ผลสัมฤทธิ์ผู้ใช้น้ำจริง</p>
                    <div class="flex items-baseline space-x-2 mt-1">
                        <span id="card-users-percent" class="text-2xl font-bold text-slate-800">53.55%</span>
                        <span class="text-xs text-red-600 font-semibold">(เป้าหมาย &ge; 90%)</span>
                    </div>
                    <p class="text-xs text-slate-400 mt-2">ประชากรเข้าถึง 5,359 คน / 10,007 คน</p>
                </div>

                <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm relative overflow-hidden">
                    <div class="absolute -right-2 -bottom-2 text-slate-100 pointer-events-none"><i data-lucide="waves" class="w-20 h-20"></i></div>
                    <p class="text-xs font-medium text-slate-500">ความเพียงพอน้ำดิบต้นทุน</p>
                    <div class="flex items-baseline space-x-2 mt-1">
                        <span id="card-water-days" class="text-2xl font-bold text-amber-600">53 วัน</span>
                        <span class="text-xs text-amber-700 font-semibold">(สระ ม.5 วิกฤต)</span>
                    </div>
                    <p class="text-xs text-slate-400 mt-2">ม.2 เหลือ 83 วัน เสี่ยงขาดแคลนในแล้ง</p>
                </div>

                <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm relative overflow-hidden">
                    <div class="absolute -right-2 -bottom-2 text-slate-100 pointer-events-none"><i data-lucide="clock" class="w-20 h-20"></i></div>
                    <p class="text-xs font-medium text-slate-500">ค่าปรับ & ดอกเบี้ยล่าช้า</p>
                    <div class="flex items-baseline space-x-2 mt-1">
                        <span id="card-penalty-day" class="text-2xl font-bold text-slate-800">124,970</span>
                        <span class="text-xs text-slate-500">บ./วัน</span>
                    </div>
                    <p class="text-xs text-slate-400 mt-2">ดอกเบี้ยเงินกู้เสียเปล่า 1,648 บ./วัน</p>
                </div>

                <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm relative overflow-hidden">
                    <div class="absolute -right-2 -bottom-2 text-slate-100 pointer-events-none"><i data-lucide="trending-down" class="w-20 h-20"></i></div>
                    <p class="text-xs font-medium text-slate-500">สถานะการเงินกิจการประปา</p>
                    <div class="flex items-baseline space-x-2 mt-1">
                        <span id="card-loss-total" class="text-2xl font-bold text-red-600">-1,301,780</span>
                        <span class="text-xs text-slate-500">บาท</span>
                    </div>
                    <p class="text-xs text-slate-400 mt-2">ค่าน้ำ 7 บ./ลบ.ม. ต่ำกว่าต้นทุนจริง</p>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm lg:col-span-2">
                    <div class="flex items-center justify-between mb-4">
                        <div>
                            <h3 class="font-heading font-semibold text-slate-800">แผนผังจัดลำดับความเสี่ยง 8 มิติ (Risk Dimension Ranking)</h3>
                            <p class="text-xs text-slate-500">ประเมินผลคูณ Impact &times; Urgency ตามแนวคิด ISO 31000/31010</p>
                        </div>
                        <span class="text-xs font-semibold px-2 py-1 bg-slate-100 rounded text-slate-600">คะแนนเต็ม 25</span>
                    </div>
                    <div class="h-72 w-full">
                        <canvas id="riskChart"></canvas>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-3">
                            <h3 class="font-heading font-semibold text-slate-800">สถานะข้อเสนอแนะ 7 ข้อ</h3>
                            <span class="text-xs px-2 py-0.5 bg-emerald-100 text-emerald-700 font-bold rounded">Action Plan</span>
                        </div>
                        <p class="text-xs text-slate-500 mb-4">ติดตามผลความคืบหน้าของหน่วยรับตรวจ</p>
                        <div class="space-y-2.5" id="action-items-container"></div>
                    </div>
                    <div class="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                        <span>แล้วเสร็จ: <b id="stat-completed" class="text-emerald-600 font-semibold">2</b> ข้อ</span>
                        <span>บางส่วน: <b id="stat-partial" class="text-amber-600 font-semibold">2</b> ข้อ</span>
                        <span>รอดำเนินการ: <b id="stat-pending" class="text-slate-600 font-semibold">3</b> ข้อ</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 1: WATER BALANCE CALCULATOR -->
        <section id="tab-water-balance" class="tab-content hidden space-y-6">
            <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 mb-4 border-b border-slate-100 gap-2">
                    <div>
                        <h2 class="text-lg font-heading font-bold text-slate-800 flex items-center gap-2">
                            <i data-lucide="droplets" class="text-blue-600 w-5 h-5"></i>
                            เครื่องคำนวณสมดุลน้ำและการประเมินความเพียงพอของแหล่งน้ำดิบ (Water Balance)
                        </h2>
                        <p class="text-xs text-slate-500">คำนวณปริมาตรกักเก็บน้ำดิบต้นทุนเปรียบเทียบอัตราการผลิตต่อวัน และคาดการณ์จำนวนวันที่ผลิตได้</p>
                    </div>
                    <button onclick="calculateWaterBalance()" class="px-4 py-2 bg-audit-600 hover:bg-audit-700 text-white rounded-lg text-xs font-semibold shadow transition">
                        คำนวณใหม่
                    </button>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-3">
                        <div class="flex items-center justify-between">
                            <h4 class="font-heading font-semibold text-slate-700 text-sm">สถานีผลิต ม.2 (สระเก็บน้ำ)</h4>
                            <span class="text-[10px] bg-blue-100 text-blue-700 px-2 py-0.5 rounded font-bold">สถานี 1</span>
                        </div>
                        <div>
                            <label class="text-xs text-slate-500 block mb-1">ปริมาตรน้ำดิบคงเหลือ (ลบ.ม.)</label>
                            <input type="number" id="wb-raw-vol-1" value="33200" class="w-full text-sm px-3 py-1.5 bg-white border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                        </div>
                        <div>
                            <label class="text-xs text-slate-500 block mb-1">อัตราผลิตเฉลี่ย (ลบ.ม./วัน)</label>
                            <input type="number" id="wb-prod-rate-1" value="400" class="w-full text-sm px-3 py-1.5 bg-white border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                        </div>
                        <div class="p-3 bg-white rounded-lg border border-slate-200 space-y-1">
                            <div class="flex justify-between text-xs">
                                <span class="text-slate-500">ผลิตได้ต่อเนื่อง:</span>
                                <span id="wb-res-days-1" class="font-bold text-amber-600">83 วัน</span>
                            </div>
                            <div class="flex justify-between text-xs">
                                <span class="text-slate-500">สถานะความเสี่ยง:</span>
                                <span id="wb-res-status-1" class="font-semibold text-amber-600">เสี่ยงขาดแคลนในฤดูแล้ง</span>
                            </div>
                        </div>
                    </div>

                    <div class="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-3">
                        <div class="flex items-center justify-between">
                            <h4 class="font-heading font-semibold text-slate-700 text-sm">สถานีผลิต ม.5 (สระเก็บน้ำ)</h4>
                            <span class="text-[10px] bg-red-100 text-red-700 px-2 py-0.5 rounded font-bold">วิกฤต</span>
                        </div>
                        <div>
                            <label class="text-xs text-slate-500 block mb-1">ปริมาตรน้ำดิบคงเหลือ (ลบ.ม.)</label>
                            <input type="number" id="wb-raw-vol-2" value="18550" class="w-full text-sm px-3 py-1.5 bg-white border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                        </div>
                        <div>
                            <label class="text-xs text-slate-500 block mb-1">อัตราผลิตเฉลี่ย (ลบ.ม./วัน)</label>
                            <input type="number" id="wb-prod-rate-2" value="350" class="w-full text-sm px-3 py-1.5 bg-white border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                        </div>
                        <div class="p-3 bg-white rounded-lg border border-slate-200 space-y-1">
                            <div class="flex justify-between text-xs">
                                <span class="text-slate-500">ผลิตได้ต่อเนื่อง:</span>
                                <span id="wb-res-days-2" class="font-bold text-red-600">53 วัน</span>
                            </div>
                            <div class="flex justify-between text-xs">
                                <span class="text-slate-500">สถานะความเสี่ยง:</span>
                                <span id="wb-res-status-2" class="font-semibold text-red-600">วิกฤตสูงมาก (&lt;60 วัน)</span>
                            </div>
                        </div>
                    </div>

                    <div class="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-3">
                        <div class="flex items-center justify-between">
                            <h4 class="font-heading font-semibold text-slate-700 text-sm">สถานีผลิต ม.3 (อ่างเก็บน้ำ)</h4>
                            <span class="text-[10px] bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded font-bold">ปกติ</span>
                        </div>
                        <div>
                            <label class="text-xs text-slate-500 block mb-1">ปริมาตรน้ำดิบคงเหลือ (ลบ.ม.)</label>
                            <input type="number" id="wb-raw-vol-3" value="115000" class="w-full text-sm px-3 py-1.5 bg-white border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                        </div>
                        <div>
                            <label class="text-xs text-slate-500 block mb-1">อัตราผลิตเฉลี่ย (ลบ.ม./วัน)</label>
                            <input type="number" id="wb-prod-rate-3" value="450" class="w-full text-sm px-3 py-1.5 bg-white border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                        </div>
                        <div class="p-3 bg-white rounded-lg border border-slate-200 space-y-1">
                            <div class="flex justify-between text-xs">
                                <span class="text-slate-500">ผลิตได้ต่อเนื่อง:</span>
                                <span id="wb-res-days-3" class="font-bold text-emerald-600">255 วัน</span>
                            </div>
                            <div class="flex justify-between text-xs">
                                <span class="text-slate-500">สถานะความเสี่ยง:</span>
                                <span id="wb-res-status-3" class="font-semibold text-emerald-600">เพียงพอตลอดปี</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="mt-6 bg-blue-50/70 border border-blue-200 p-4 rounded-xl">
                    <h4 class="text-xs font-bold text-blue-900 uppercase tracking-wide flex items-center gap-1.5">
                        <i data-lucide="info" class="w-4 h-4"></i> สรุปข้อวิเคราะห์ทางวิศวกรรมการตรวจเงินแผ่นดิน
                    </h4>
                    <p class="text-xs text-blue-800 mt-1 leading-relaxed">
                        จากการคำนวณสมดุลน้ำพบว่า สถานี ม.5 และ ม.2 มีปริมาณน้ำดิบต้นทุนไม่เพียงพอต่อการเดินระบบต่อเนื่องตลอดปีงบประมาณ ทำให้ อบต. ต้องตั้งงบประมาณขอขุดลอกสระเก็บน้ำเพิ่มเติมในปี 2570 เป็นเงินถึง 29.50 ล้านบาท สะท้อนถึงการขาดการวางแผนจัดหาแหล่งน้ำดิบสำรองก่อนดำเนินโครงการเงินกู้ 49.98 ล้านบาท
                    </p>
                </div>
            </div>
        </section>

        <!-- TAB 2: SAMPLING CALCULATOR -->
        <section id="tab-sampling" class="tab-content hidden space-y-6">
            <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
                <div class="pb-4 mb-4 border-b border-slate-100">
                    <h2 class="text-lg font-heading font-bold text-slate-800 flex items-center gap-2">
                        <i data-lucide="calculator" class="text-audit-500 w-5 h-5"></i>
                        เครื่องคำนวณขนาดตัวอย่าง Cochran (1977) และการจัดสรรตามสัดส่วนแบบชั้นภูมิ
                    </h2>
                    <p class="text-xs text-slate-500">สำหรับกำหนดกลุ่มตัวอย่างครัวเรือนผู้ใช้น้ำ พร้อมปรับแก้สำหรับประชากรที่มีขนาดจำกัด (Finite Population)</p>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <div class="space-y-4">
                        <div class="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-3">
                            <h4 class="font-semibold text-xs text-slate-700 uppercase">กำหนดพารามิเตอร์ทางสถิติ</h4>
                            <div class="grid grid-cols-2 gap-3">
                                <div>
                                    <label class="text-xs text-slate-500 block">จำนวนประชากรทั้งหมด (N)</label>
                                    <input type="number" id="sam-N" value="2290" oninput="calculateSampling()" class="w-full text-sm px-3 py-1.5 bg-white border border-slate-300 rounded-lg">
                                </div>
                                <div>
                                    <label class="text-xs text-slate-500 block">ระดับความเชื่อมั่น (Z-Score)</label>
                                    <select id="sam-Z" onchange="calculateSampling()" class="w-full text-sm px-3 py-1.5 bg-white border border-slate-300 rounded-lg">
                                        <option value="1.96">95% (Z = 1.96)</option>
                                        <option value="1.645">90% (Z = 1.645)</option>
                                        <option value="2.576">99% (Z = 2.576)</option>
                                    </select>
                                </div>
                                <div>
                                    <label class="text-xs text-slate-500 block">สัดส่วนประชากรที่สนใจ (p)</label>
                                    <input type="number" id="sam-p" value="0.5" step="0.05" oninput="calculateSampling()" class="w-full text-sm px-3 py-1.5 bg-white border border-slate-300 rounded-lg">
                                </div>
                                <div>
                                    <label class="text-xs text-slate-500 block">ความคลาดเคลื่อนที่ยอมรับ (e)</label>
                                    <input type="number" id="sam-e" value="0.18" step="0.01" oninput="calculateSampling()" class="w-full text-sm px-3 py-1.5 bg-white border border-slate-300 rounded-lg">
                                </div>
                            </div>
                        </div>

                        <div class="p-4 bg-emerald-50 border border-emerald-200 rounded-xl space-y-2">
                            <div class="flex justify-between items-center">
                                <span class="text-xs text-emerald-800">ขนาดตัวอย่างขั้นต้น (n₀):</span>
                                <span id="sam-n0-res" class="text-sm font-mono font-bold text-emerald-900">30.07</span>
                            </div>
                            <div class="flex justify-between items-center">
                                <span class="text-xs text-emerald-800">ปรับแก้ด้วย Finite Population (n):</span>
                                <span id="sam-n-adj-res" class="text-sm font-mono font-bold text-emerald-900">29.69</span>
                            </div>
                            <div class="flex justify-between items-center pt-2 border-t border-emerald-200/60">
                                <span class="text-xs font-bold text-emerald-900">ขนาดตัวอย่างสุทธิที่ต้องสุ่ม (ปัดเศษ):</span>
                                <span id="sam-final-res" class="text-2xl font-heading font-bold text-emerald-700">30 ตัวอย่าง</span>
                            </div>
                        </div>
                    </div>

                    <div class="space-y-3">
                        <h4 class="font-semibold text-xs text-slate-700 uppercase flex items-center justify-between">
                            <span>การจัดสรรตัวอย่างตามสัดส่วนชั้นภูมิ (Proportional Stratified)</span>
                            <span class="text-slate-400 font-normal text-[11px]">สูตร: n_h = (N_h / N) &times; n</span>
                        </h4>
                        <div class="overflow-x-auto border border-slate-200 rounded-xl">
                            <table class="w-full text-left text-xs">
                                <thead class="bg-slate-50 text-slate-600 border-b border-slate-200">
                                    <tr>
                                        <th class="px-3 py-2">หมู่บ้าน / ชั้นภูมิ</th>
                                        <th class="px-3 py-2 text-right">ครัวเรือน (N_h)</th>
                                        <th class="px-3 py-2 text-right">สัดส่วน (%)</th>
                                        <th class="px-3 py-2 text-right bg-emerald-50 text-emerald-900">ตัวอย่าง (n_h)</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-100" id="stratified-tbody"></tbody>
                                <tfoot class="bg-slate-50 font-bold text-slate-700 border-t border-slate-200">
                                    <tr>
                                        <td class="px-3 py-2">รวมทั้งหมด</td>
                                        <td class="px-3 py-2 text-right" id="strat-sum-nh">2,290</td>
                                        <td class="px-3 py-2 text-right">100.0%</td>
                                        <td class="px-3 py-2 text-right bg-emerald-100/70 text-emerald-900" id="strat-sum-n">30 ตัวอย่าง</td>
                                    </tr>
                                </tfoot>
                            </table>
                        </div>
                        <p class="text-[11px] text-slate-400 leading-tight">
                            *ข้อมูลตรงตามเอกสารรายงานผลการตรวจสอบของ อบต.ไชยราช ที่ใช้สุ่มสัมภาษณ์ 30 ครัวเรือน
                        </p>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 3: FINANCIAL & DELAY ANALYSIS -->
        <section id="tab-financial" class="tab-content hidden space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
                    <div class="pb-3 border-b border-slate-100">
                        <h3 class="font-heading font-bold text-slate-800 flex items-center gap-2">
                            <i data-lucide="alert-triangle" class="text-amber-500 w-5 h-5"></i>
                            การวิเคราะห์ค่าปรับสัญญาและความล่าช้า (Delay Analysis)
                        </h3>
                        <p class="text-xs text-slate-500">ประเมินภาระค่าปรับตาม พ.ร.บ. จัดซื้อจัดจ้างฯ และภาระดอกเบี้ยเงินกู้สูญเปล่า</p>
                    </div>

                    <div class="space-y-3">
                        <div>
                            <label class="text-xs text-slate-500 block mb-1">วงเงินตามสัญญาจ้าง (บาท)</label>
                            <input type="number" id="fin-contract-val" value="49988000" oninput="calculateFinancials()" class="w-full text-sm px-3 py-1.5 border border-slate-300 rounded-lg">
                        </div>
                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="text-xs text-slate-500 block mb-1">อัตราค่าปรับ/วัน (%)</label>
                                <input type="number" id="fin-penalty-rate" value="0.25" step="0.05" oninput="calculateFinancials()" class="w-full text-sm px-3 py-1.5 border border-slate-300 rounded-lg">
                            </div>
                            <div>
                                <label class="text-xs text-slate-500 block mb-1">จำนวนวันส่งมอบล่าช้า</label>
                                <input type="number" id="fin-delay-days" value="7" oninput="calculateFinancials()" class="w-full text-sm px-3 py-1.5 border border-slate-300 rounded-lg">
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="text-xs text-slate-500 block mb-1">อัตราดอกเบี้ยเงินกู้ (% ต่อปี)</label>
                                <input type="number" id="fin-loan-interest" value="2.00" step="0.1" oninput="calculateFinancials()" class="w-full text-sm px-3 py-1.5 border border-slate-300 rounded-lg">
                            </div>
                            <div>
                                <label class="text-xs text-slate-500 block mb-1">ล่าช้าก่อนเปิดใช้งาน (วัน)</label>
                                <input type="number" id="fin-idle-days" value="30" oninput="calculateFinancials()" class="w-full text-sm px-3 py-1.5 border border-slate-300 rounded-lg">
                            </div>
                        </div>
                    </div>

                    <div class="bg-amber-50 p-4 rounded-xl border border-amber-200 space-y-2">
                        <div class="flex justify-between text-xs">
                            <span class="text-amber-900">อัตราค่าปรับต่อวัน:</span>
                            <span id="fin-res-penalty-day" class="font-mono font-bold text-amber-900">124,970.00 บาท/วัน</span>
                        </div>
                        <div class="flex justify-between text-xs">
                            <span class="text-amber-900">ประมาณการค่าปรับรวม (7 วัน):</span>
                            <span id="fin-res-penalty-total" class="font-mono font-bold text-amber-900">874,790.00 บาท</span>
                        </div>
                        <div class="flex justify-between text-xs pt-2 border-t border-amber-200">
                            <span class="text-amber-900">ดอกเบี้ยเงินกู้สูญเปล่าต่อวัน:</span>
                            <span id="fin-res-interest-day" class="font-mono font-bold text-red-700">1,648.16 บาท/วัน</span>
                        </div>
                        <div class="flex justify-between text-xs">
                            <span class="text-amber-900 font-bold">ดอกเบี้ยสูญเปล่าช่วงทิ้งร้าง (30 วัน):</span>
                            <span id="fin-res-interest-total" class="font-mono font-bold text-red-700">49,444.80 บาท</span>
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
                    <div class="pb-3 border-b border-slate-100">
                        <h3 class="font-heading font-bold text-slate-800 flex items-center gap-2">
                            <i data-lucide="pie-chart" class="text-red-500 w-5 h-5"></i>
                            ความยั่งยืนทางการเงินและต้นทุนต่อหน่วย (Unit Cost)
                        </h3>
                        <p class="text-xs text-slate-500">วิเคราะห์ผลประกอบการกิจการประปา อบต.ไชยราช (ปีงบประมาณ 2569)</p>
                    </div>

                    <div class="space-y-3">
                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="text-xs text-slate-500 block mb-1">รายรับค่าน้ำประปา (บาท)</label>
                                <input type="number" id="fin-revenue" value="1348878" oninput="calculateFinancials()" class="w-full text-sm px-3 py-1.5 border border-slate-300 rounded-lg">
                            </div>
                            <div>
                                <label class="text-xs text-slate-500 block mb-1">รายจ่ายดำเนินการรวม (บาท)</label>
                                <input type="number" id="fin-expense" value="2650658.67" oninput="calculateFinancials()" class="w-full text-sm px-3 py-1.5 border border-slate-300 rounded-lg">
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="text-xs text-slate-500 block mb-1">ปริมาณน้ำที่จำหน่าย (ลบ.ม.)</label>
                                <input type="number" id="fin-vol-sold" value="192696" oninput="calculateFinancials()" class="w-full text-sm px-3 py-1.5 border border-slate-300 rounded-lg">
                            </div>
                            <div>
                                <label class="text-xs text-slate-500 block mb-1">อัตราค่าน้ำที่จัดเก็บ (บ./ลบ.ม.)</label>
                                <input type="number" id="fin-tariff" value="7.00" step="0.5" oninput="calculateFinancials()" class="w-full text-sm px-3 py-1.5 border border-slate-300 rounded-lg">
                            </div>
                        </div>
                    </div>

                    <div class="bg-red-50 p-4 rounded-xl border border-red-200 space-y-2">
                        <div class="flex justify-between text-xs">
                            <span class="text-red-900">ผลการดำเนินงานสุทธิ (ขาดทุน):</span>
                            <span id="fin-res-deficit" class="font-mono font-bold text-red-700">-1,301,780.67 บาท</span>
                        </div>
                        <div class="flex justify-between text-xs">
                            <span class="text-red-900">ต้นทุนการผลิตจริงต่อหน่วย:</span>
                            <span id="fin-res-unit-cost" class="font-mono font-bold text-red-700">13.76 บาท/ลบ.ม.</span>
                        </div>
                        <div class="flex justify-between text-xs pt-2 border-t border-red-200">
                            <span class="text-red-900 font-bold">อัตราค่าน้ำที่ควรปรับปรุง:</span>
                            <span class="font-mono font-bold text-red-800">ไม่ต่ำกว่า 13.80 บ./ลบ.ม.</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 4: UNDERGROUND PIPELINE LOG -->
        <section id="tab-pipeline" class="tab-content hidden space-y-6">
            <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 mb-4 border-b border-slate-100 gap-2">
                    <div>
                        <h2 class="text-lg font-heading font-bold text-slate-800 flex items-center gap-2">
                            <i data-lucide="map-pinned" class="text-audit-600 w-5 h-5"></i>
                            ตารางบันทึกหลักฐานเชิงตำแหน่งสำหรับงานโครงสร้างใต้ดิน (Underground Pipeline Inspection Log)
                        </h2>
                        <p class="text-xs text-slate-500">บันทึกผลตรวจสอบท่อเมนประปา HDPE 25 กิโลเมตร ที่ถูกกลบดินแล้ว โดยอ้างอิงบ่อพัก (Manhole) และไมล์ กม.</p>
                    </div>
                    <button onclick="addPipelineRow()" class="inline-flex items-center space-x-1 px-3 py-1.5 bg-audit-600 hover:bg-audit-700 text-white rounded-lg text-xs font-semibold shadow transition">
                        <i data-lucide="plus" class="w-3.5 h-3.5"></i>
                        <span>เพิ่มจุดตรวจ</span>
                    </button>
                </div>

                <div class="overflow-x-auto border border-slate-200 rounded-xl custom-scrollbar">
                    <table class="w-full text-left text-xs whitespace-nowrap">
                        <thead class="bg-slate-50 text-slate-700 font-semibold border-b border-slate-200">
                            <tr>
                                <th class="px-3 py-2.5">จุดตรวจสอบ / กม.</th>
                                <th class="px-3 py-2.5">พิกัด GPS / ทางหลวง</th>
                                <th class="px-3 py-2.5">ชนิด & ขนาดท่อ (แบบ)</th>
                                <th class="px-3 py-2.5">ตรวจพบจริงที่บ่อพัก</th>
                                <th class="px-3 py-2.5">ชั้นแรงดัน (PN)</th>
                                <th class="px-3 py-2.5 text-center">อุปกรณ์ประกอบ (PRV/Air Valve)</th>
                                <th class="px-3 py-2.5 text-center">สถานะความสอดคล้อง</th>
                                <th class="px-3 py-2.5 text-center">จัดการ</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100" id="pipeline-tbody"></tbody>
                    </table>
                </div>
                
                <div class="mt-4 p-3 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-800 flex items-start gap-2">
                    <i data-lucide="shield-check" class="w-4 h-4 text-amber-600 mt-0.5 flex-shrink-0"></i>
                    <div>
                        <b>ข้อสังเกตวิศวกรผู้ตรวจสอบ:</b> การกลบดินทับแนวท่อเมนโดยไม่มีการตรวจสอบแนวท่อร่วมกับช่างผู้ควบคุมงาน ทำให้ไม่สามารถตรวจสอบความหนาชั้นทรายรองท่อ (Bedding) ได้โดยตรง จึงต้องใช้เทคนิค Cross-Check ตำแหน่ง Stub-end, หน้าจาน, และฝาบ่อพัก PRV เทียบภาพถ่ายดาวเทียมเพื่อยืนยันพยานหลักฐาน
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 5: CHECKLIST & RISK MATRIX -->
        <section id="tab-checklist" class="tab-content hidden space-y-6">
            <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 mb-4 border-b border-slate-100 gap-2">
                    <div>
                        <h2 class="text-lg font-heading font-bold text-slate-800 flex items-center gap-2">
                            <i data-lucide="clipboard-check" class="text-audit-600 w-5 h-5"></i>
                            แบบประเมินความเสี่ยง 8 มิติ (ISO 31000 / 31010 Risk Matrix Assessment)
                        </h2>
                        <p class="text-xs text-slate-500">คำนวณคะแนนความเสี่ยง = ระดับผลกระทบ (Impact 1-5) &times; ระดับความเร่งด่วน (Urgency 1-5)</p>
                    </div>
                    <button onclick="recalculateAllRiskScores()" class="px-4 py-2 bg-audit-600 hover:bg-audit-700 text-white rounded-lg text-xs font-semibold shadow transition">
                        บันทึก & อัปเดตแดชบอร์ด
                    </button>
                </div>

                <div class="overflow-x-auto border border-slate-200 rounded-xl">
                    <table class="w-full text-left text-xs">
                        <thead class="bg-slate-50 text-slate-700 font-semibold border-b border-slate-200">
                            <tr>
                                <th class="px-3 py-2.5 w-12 text-center">มิติ</th>
                                <th class="px-3 py-2.5">ประเด็นความเสี่ยงในการตรวจสอบ</th>
                                <th class="px-3 py-2.5 w-24 text-center">Impact (1-5)</th>
                                <th class="px-3 py-2.5 w-24 text-center">Urgency (1-5)</th>
                                <th class="px-3 py-2.5 w-24 text-center">คะแนนเสี่ยง</th>
                                <th class="px-3 py-2.5 w-28 text-center">ระดับความเสี่ยง</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100" id="risk-matrix-tbody"></tbody>
                    </table>
                </div>

                <div class="mt-6 grid grid-cols-1 md:grid-cols-4 gap-3 text-center">
                    <div class="p-3 bg-red-100/70 border border-red-300 rounded-xl">
                        <span class="text-xs font-bold text-red-800 block">วิกฤตสูงมาก (16 - 25)</span>
                        <span class="text-[11px] text-red-700">ต้องสั่งการแก้ไขทันที / แจ้งข้อเสนอแนะเร่งด่วน</span>
                    </div>
                    <div class="p-3 bg-amber-100/70 border border-amber-300 rounded-xl">
                        <span class="text-xs font-bold text-amber-800 block">สูง (10 - 15)</span>
                        <span class="text-[11px] text-amber-700">มีผลกระทบต่อผลสัมฤทธิ์อย่างมีนัยสำคัญ</span>
                    </div>
                    <div class="p-3 bg-blue-100/70 border border-blue-300 rounded-xl">
                        <span class="text-xs font-bold text-blue-800 block">ปานกลาง (5 - 9)</span>
                        <span class="text-[11px] text-blue-700">ต้องปรับปรุงแนวปฏิบัติและการบริหารจัดการ</span>
                    </div>
                    <div class="p-3 bg-emerald-100/70 border border-emerald-300 rounded-xl">
                        <span class="text-xs font-bold text-emerald-800 block">ต่ำ (1 - 4)</span>
                        <span class="text-[11px] text-emerald-700">เป็นไปตามเกณฑ์มาตรฐานหรือบกพร่องเล็กน้อย</span>
                    </div>
                </div>
            </div>
        </section>

    </main>

    <footer class="bg-white border-t border-slate-200 py-4 text-center text-xs text-slate-500 no-print">
        <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
            <span>สำนักงานการตรวจเงินแผ่นดินภูมิภาคที่ ๑๒ • สำนักตรวจเงินแผ่นดินจังหวัดประจวบคีรีขันธ์</span>
            <span class="font-medium text-slate-700">Water Supply Audit Risk Tool (v1.0 Prototyping)</span>
        </div>
    </footer>

    <script>
        let riskChartInstance = null;

        const initialRiskDimensions = [
            { id: 1, name: '1. ความเพียงพอแหล่งน้ำดิบ', impact: 4, urgency: 5, score: 20, desc: 'น้ำดิบ ม.5 เหลือ 53 วัน ม.2 เหลือ 83 วัน เสี่ยงขาดแคลนในแล้ง' },
            { id: 2, name: '2. คุณภาพน้ำประปา', impact: 4, urgency: 4, score: 16, desc: 'คลอรีนปลายท่อ 0.01-0.09 ต่ำกว่าเกณฑ์ และแมงกานีสเกินมาตรฐาน' },
            { id: 3, name: '3. ผลสัมฤทธิ์ผู้ใช้น้ำ', impact: 5, urgency: 4, score: 20, desc: 'ผู้ใช้น้ำจริง 53.55% ต่ำกว่าเป้าหมายที่กำหนดไว้ไม่น้อยกว่า 90%' },
            { id: 4, name: '4. ระบบควบคุมนวัตกรรม', impact: 4, urgency: 3, score: 12, desc: 'Line Notify และ VSD ยังไม่เปิดใช้งานจริงเนื่องจากไม่มี SIM Card' },
            { id: 5, name: '5. ความครบถ้วนอุปกรณ์', impact: 3, urgency: 3, score: 9, desc: 'เครื่องวัดความขุ่น/คลอรีนขาดหาย ฝาบ่อพัก PRV ไม่ตรงแบบ' },
            { id: 6, name: '6. ความล่าช้าสัญญา & ดอกเบี้ย', impact: 3, urgency: 3, score: 9, desc: 'ส่งมอบช้า 7 วัน อนุมัติขยาย 15 วันไม่รัดกุม ทิ้งร้าง 1 เดือน' },
            { id: 7, name: '7. การบริหารพัสดุครุภัณฑ์', impact: 3, urgency: 4, score: 12, desc: 'ไม่แยกทะเบียนสินทรัพย์ พ.ด.1 3 สถานี ไม่มีทะเบียนคุมสารเคมี' },
            { id: 8, name: '8. ความยั่งยืนทางการเงิน', impact: 4, urgency: 4, score: 16, desc: 'ขาดทุน 1.3 ล้านบาท ค่าน้ำ 7 บาทต่ำกว่าต้นทุนจริง 13.76 บาท' }
        ];

        const initialStrata = [
            { village: 'หมู่ที่ 1 บ้านไชยราช', households: 420 },
            { village: 'หมู่ที่ 2 บ้านสวนหลวง', households: 580 },
            { village: 'หมู่ที่ 3 บ้านหินเทิน', households: 390 },
            { village: 'หมู่ที่ 4 บ้านห้วยคล้า', households: 480 },
            { village: 'หมู่ที่ 5 บ้านไร่ใน', households: 420 }
        ];

        let pipelineData = [
            { id: 1, station: 'กม. 0+000 (สถานีผลิต ม.2)', location: 'ถ.ทางหลวงชนบท ปข.2005', planPipe: 'HDPE 225 มม.', actualPipe: 'HDPE 225 มม.', pn: 'PN 10', valve: 'Combination Air Valve', match: true },
            { id: 2, station: 'กม. 4+250 (จุดตัด ม.2 - ม.3)', location: 'บ่อพัก PRV-01', planPipe: 'HDPE 160 มม.', actualPipe: 'HDPE 160 มม.', pn: 'PN 8', valve: 'PRV (ฝาบ่อชำรุด)', match: false },
            { id: 3, station: 'กม. 12+800 (สถานีเพิ่มแรงดัน)', location: 'Booster Pump Station', planPipe: 'HDPE 160 มม.', actualPipe: 'HDPE 160 มม.', pn: 'PN 10', valve: 'Check Valve / Air Valve', match: true },
            { id: 4, station: 'กม. 18+500 (ทางแยก ม.4)', location: 'บ่อพักหน้าโรงเรียน', planPipe: 'HDPE 110 มม.', actualPipe: 'HDPE 110 มม.', pn: 'PN 6', valve: 'Gate Valve 110 มม.', match: true },
            { id: 5, station: 'กม. 24+950 (ปลายท่อ ม.5)', location: 'จุดล้างท่อ Blow-off', planPipe: 'HDPE 110 มม.', actualPipe: 'HDPE 110 มม.', pn: 'PN 6', valve: 'Blow-off Valve', match: true }
        ];

        const actionItems = [
            { no: 1, title: 'สำรวจครัวเรือนผู้ใช้น้ำ & จัดหาแหล่งน้ำดิบสำรอง', status: 'pending', label: 'อยู่ระหว่างดำเนินการ' },
            { no: 2, title: 'ปรับปรุงคุณภาพน้ำประปา (คลอรีน & แมงกานีส)', status: 'completed', label: 'ดำเนินการแล้วเสร็จ' },
            { no: 3, title: 'เปิดใช้ Line Notify, VSD & ติดตั้งหม้อแปลง ม.2', status: 'completed', label: 'ดำเนินการแล้วเสร็จ' },
            { no: 4, title: 'จัดทำบัญชีต้นทุนการผลิตน้ำประปาต่อหน่วย', status: 'pending', label: 'อยู่ระหว่างดำเนินการ' },
            { no: 5, title: 'ลงทะเบียนคุมพัสดุ พ.ด.1 & ทะเบียนสารเคมี', status: 'partial', label: 'แล้วเสร็จบางส่วน (กองคลัง)' },
            { no: 6, title: 'แก้ไขอุปกรณ์ไม่ตรงแบบ (วัดความขุ่น/ฝา PRV)', status: 'partial', label: 'แล้วเสร็จบางส่วน' },
            { no: 7, title: 'กำชับระเบียบพิจารณาขยายระยะเวลาสัญญา', status: 'pending', label: 'อยู่ระหว่างดำเนินการ' }
        ];

        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('bg-white/20', 'text-white', 'shadow');
                btn.classList.add('text-slate-200');
            });

            const targetTab = document.getElementById(`tab-${tabId}`);
            if (targetTab) targetTab.classList.remove('hidden');

            const activeBtn = document.querySelector(`.tab-btn[data-tab="${tabId}"]`);
            if (activeBtn) {
                activeBtn.classList.add('bg-white/20', 'text-white', 'shadow');
                activeBtn.classList.remove('text-slate-200');
            }

            if (tabId === 'dashboard' && riskChartInstance) {
                setTimeout(() => riskChartInstance.resize(), 100);
            }
        }

        function initRiskChart() {
            const ctx = document.getElementById('riskChart').getContext('2d');
            const sorted = [...initialRiskDimensions].sort((a, b) => b.score - a.score);
            const labels = sorted.map(d => d.name);
            const data = sorted.map(d => d.score);
            const colors = data.map(val => {
                if (val >= 16) return 'rgba(220, 38, 38, 0.85)';
                if (val >= 10) return 'rgba(217, 119, 6, 0.85)';
                if (val >= 5) return 'rgba(37, 99, 235, 0.85)';
                return 'rgba(16, 185, 129, 0.85)';
            });

            if (riskChartInstance) riskChartInstance.destroy();

            riskChartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'คะแนนความเสี่ยง (Impact × Urgency)',
                        data: data,
                        backgroundColor: colors,
                        borderRadius: 6,
                        borderWidth: 0
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            beginAtZero: true,
                            max: 25,
                            ticks: { stepSize: 5 }
                        }
                    },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                afterLabel: function(context) {
                                    const item = sorted[context.dataIndex];
                                    return `ผลกระทบ: ${item.impact} | ความเร่งด่วน: ${item.urgency}\\nรายละเอียด: ${item.desc}`;
                                }
                            }
                        }
                    }
                }
            });
        }

        function renderActionTracker() {
            const container = document.getElementById('action-items-container');
            container.innerHTML = '';
            let completed = 0, partial = 0, pending = 0;

            actionItems.forEach(item => {
                let badgeClass = 'bg-slate-100 text-slate-600';
                if (item.status === 'completed') {
                    badgeClass = 'bg-emerald-100 text-emerald-800 font-semibold';
                    completed++;
                } else if (item.status === 'partial') {
                    badgeClass = 'bg-amber-100 text-amber-800 font-semibold';
                    partial++;
                } else {
                    pending++;
                }

                const div = document.createElement('div');
                div.className = 'flex items-center justify-between text-xs p-2 rounded-lg bg-slate-50 border border-slate-100';
                div.innerHTML = `
                    <div class="flex items-center space-x-2 truncate mr-2">
                        <span class="w-5 h-5 rounded-full bg-slate-200 text-slate-700 flex items-center justify-center font-bold text-[10px] flex-shrink-0">${item.no}</span>
                        <span class="truncate text-slate-700 font-medium">${item.title}</span>
                    </div>
                    <span class="px-2 py-0.5 rounded text-[10px] whitespace-nowrap ${badgeClass}">${item.label}</span>
                `;
                container.appendChild(div);
            });

            document.getElementById('stat-completed').innerText = completed;
            document.getElementById('stat-partial').innerText = partial;
            document.getElementById('stat-pending').innerText = pending;
        }

        function calculateWaterBalance() {
            for (let i = 1; i <= 3; i++) {
                const vol = parseFloat(document.getElementById(`wb-raw-vol-${i}`).value) || 0;
                const rate = parseFloat(document.getElementById(`wb-prod-rate-${i}`).value) || 1;
                const days = Math.floor(vol / rate);

                const daysEl = document.getElementById(`wb-res-days-${i}`);
                const statusEl = document.getElementById(`wb-res-status-${i}`);

                daysEl.innerText = `${days} วัน`;

                if (days < 60) {
                    daysEl.className = 'font-bold text-red-600';
                    statusEl.innerText = 'วิกฤตสูงมาก (<60 วัน)';
                    statusEl.className = 'font-semibold text-red-600';
                } else if (days < 100) {
                    daysEl.className = 'font-bold text-amber-600';
                    statusEl.innerText = 'เสี่ยงขาดแคลนในฤดูแล้ง';
                    statusEl.className = 'font-semibold text-amber-600';
                } else {
                    daysEl.className = 'font-bold text-emerald-600';
                    statusEl.innerText = 'เพียงพอตลอดปี';
                    statusEl.className = 'font-semibold text-emerald-600';
                }
            }
        }

        function calculateSampling() {
            const N = parseFloat(document.getElementById('sam-N').value) || 2290;
            const Z = parseFloat(document.getElementById('sam-Z').value) || 1.96;
            const p = parseFloat(document.getElementById('sam-p').value) || 0.5;
            const e = parseFloat(document.getElementById('sam-e').value) || 0.18;

            const q = 1 - p;
            const n0 = (Math.pow(Z, 2) * p * q) / Math.pow(e, 2);
            const n_adj = n0 / (1 + ((n0 - 1) / N));
            const n_final = Math.ceil(n_adj);

            document.getElementById('sam-n0-res').innerText = n0.toFixed(2);
            document.getElementById('sam-n-adj-res').innerText = n_adj.toFixed(2);
            document.getElementById('sam-final-res').innerText = `${n_final} ตัวอย่าง`;

            const tbody = document.getElementById('stratified-tbody');
            tbody.innerHTML = '';
            let sumN = 0;
            let sumAllocated = 0;

            initialStrata.forEach((stratum, idx) => {
                sumN += stratum.households;
                const ratio = stratum.households / N;
                let nh = Math.round(ratio * n_final);
                if (idx === initialStrata.length - 1) {
                    nh = n_final - sumAllocated;
                } else {
                    sumAllocated += nh;
                }

                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td class="px-3 py-2 font-medium text-slate-800">${stratum.village}</td>
                    <td class="px-3 py-2 text-right">${stratum.households.toLocaleString()}</td>
                    <td class="px-3 py-2 text-right">${(ratio * 100).toFixed(1)}%</td>
                    <td class="px-3 py-2 text-right font-bold text-emerald-800 bg-emerald-50/50">${nh} ครัวเรือน</td>
                `;
                tbody.appendChild(tr);
            });

            document.getElementById('strat-sum-nh').innerText = sumN.toLocaleString();
            document.getElementById('strat-sum-n').innerText = `${n_final} ตัวอย่าง`;
        }

        function calculateFinancials() {
            const contractVal = parseFloat(document.getElementById('fin-contract-val').value) || 0;
            const penaltyRate = parseFloat(document.getElementById('fin-penalty-rate').value) || 0;
            const delayDays = parseFloat(document.getElementById('fin-delay-days').value) || 0;
            const loanRate = parseFloat(document.getElementById('fin-loan-interest').value) || 0;
            const idleDays = parseFloat(document.getElementById('fin-idle-days').value) || 0;

            const penaltyPerDay = contractVal * (penaltyRate / 100);
            const totalPenalty = penaltyPerDay * delayDays;

            const interestPerDay = (contractVal * (loanRate / 100)) / 365;
            const totalInterestIdle = interestPerDay * idleDays;

            document.getElementById('fin-res-penalty-day').innerText = `${penaltyPerDay.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })} บาท/วัน`;
            document.getElementById('fin-res-penalty-total').innerText = `${totalPenalty.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })} บาท`;
            document.getElementById('fin-res-interest-day').innerText = `${interestPerDay.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })} บาท/วัน`;
            document.getElementById('fin-res-interest-total').innerText = `${totalInterestIdle.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })} บาท`;

            const rev = parseFloat(document.getElementById('fin-revenue').value) || 0;
            const exp = parseFloat(document.getElementById('fin-expense').value) || 0;
            const vol = parseFloat(document.getElementById('fin-vol-sold').value) || 1;

            const deficit = rev - exp;
            const unitCost = exp / vol;

            document.getElementById('fin-res-deficit').innerText = `${deficit.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })} บาท`;
            document.getElementById('fin-res-unit-cost').innerText = `${unitCost.toFixed(2)} บาท/ลบ.ม.`;
        }

        function renderPipelineTable() {
            const tbody = document.getElementById('pipeline-tbody');
            tbody.innerHTML = '';

            pipelineData.forEach((row, index) => {
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-50 transition';
                tr.innerHTML = `
                    <td class="px-3 py-2.5 font-medium text-slate-800">${row.station}</td>
                    <td class="px-3 py-2.5 text-slate-600">${row.location}</td>
                    <td class="px-3 py-2.5 font-mono text-slate-700">${row.planPipe}</td>
                    <td class="px-3 py-2.5 font-mono text-slate-700">${row.actualPipe}</td>
                    <td class="px-3 py-2.5 font-semibold text-slate-600">${row.pn}</td>
                    <td class="px-3 py-2.5 text-center text-slate-700">${row.valve}</td>
                    <td class="px-3 py-2.5 text-center">
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold ${row.match ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-800'}">
                            ${row.match ? 'สอดคล้องตามแบบ' : 'ไม่สอดคล้อง / ชำรุด'}
                        </span>
                    </td>
                    <td class="px-3 py-2.5 text-center">
                        <button onclick="removePipelineRow(${index})" class="text-slate-400 hover:text-red-600 transition p-1">
                            <i data-lucide="trash-2" class="w-4 h-4"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
            lucide.createIcons();
        }

        function addPipelineRow() {
            const newPt = prompt("ระบุจุดตรวจสอบและ กม. ใหม่ (เช่น กม. 7+500 บ่อพัก ม.3):", "กม. 7+500 บ่อพัก ม.3");
            if (newPt) {
                pipelineData.push({
                    id: pipelineData.length + 1,
                    station: newPt,
                    location: 'แนวท่อเมน HDPE',
                    planPipe: 'HDPE 160 มม.',
                    actualPipe: 'HDPE 160 มม.',
                    pn: 'PN 8',
                    valve: 'Gate Valve',
                    match: true
                });
                renderPipelineTable();
            }
        }

        function removePipelineRow(index) {
            pipelineData.splice(index, 1);
            renderPipelineTable();
        }

        function renderRiskMatrixTable() {
            const tbody = document.getElementById('risk-matrix-tbody');
            tbody.innerHTML = '';

            initialRiskDimensions.forEach((item, index) => {
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-50 transition';
                
                let badgeClass = 'bg-emerald-100 text-emerald-800';
                let statusText = 'ต่ำ';
                if (item.score >= 16) {
                    badgeClass = 'bg-red-100 text-red-800 font-bold';
                    statusText = 'วิกฤตสูงมาก';
                } else if (item.score >= 10) {
                    badgeClass = 'bg-amber-100 text-amber-800 font-bold';
                    statusText = 'สูง';
                } else if (item.score >= 5) {
                    badgeClass = 'bg-blue-100 text-blue-800 font-semibold';
                    statusText = 'ปานกลาง';
                }

                tr.innerHTML = `
                    <td class="px-3 py-2.5 text-center font-bold text-slate-500">${item.id}</td>
                    <td class="px-3 py-2.5">
                        <div class="font-medium text-slate-800">${item.name}</div>
                        <div class="text-[11px] text-slate-500">${item.desc}</div>
                    </td>
                    <td class="px-3 py-2.5 text-center">
                        <input type="number" min="1" max="5" value="${item.impact}" onchange="updateMatrixItem(${index}, 'impact', this.value)" class="w-14 text-center border border-slate-300 rounded p-1 text-xs">
                    </td>
                    <td class="px-3 py-2.5 text-center">
                        <input type="number" min="1" max="5" value="${item.urgency}" onchange="updateMatrixItem(${index}, 'urgency', this.value)" class="w-14 text-center border border-slate-300 rounded p-1 text-xs">
                    </td>
                    <td class="px-3 py-2.5 text-center font-bold font-mono text-slate-800 text-sm">
                        ${item.score}
                    </td>
                    <td class="px-3 py-2.5 text-center">
                        <span class="px-2 py-0.5 rounded text-[10px] ${badgeClass}">${statusText}</span>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        function updateMatrixItem(index, key, val) {
            val = parseInt(val) || 1;
            if (val > 5) val = 5;
            if (val < 1) val = 1;

            initialRiskDimensions[index][key] = val;
            initialRiskDimensions[index].score = initialRiskDimensions[index].impact * initialRiskDimensions[index].urgency;
            renderRiskMatrixTable();
            recalculateAllRiskScores();
        }

        function recalculateAllRiskScores() {
            let total = 0;
            let critical = 0;

            initialRiskDimensions.forEach(item => {
                total += item.score;
                if (item.score >= 16) critical++;
            });

            document.getElementById('total-risk-score').innerText = total;
            document.getElementById('critical-risk-count').innerText = critical;

            initRiskChart();
        }

        function loadSampleData() {
            document.getElementById('wb-raw-vol-1').value = 33200;
            document.getElementById('wb-prod-rate-1').value = 400;
            document.getElementById('wb-raw-vol-2').value = 18550;
            document.getElementById('wb-prod-rate-2').value = 350;
            document.getElementById('wb-raw-vol-3').value = 115000;
            document.getElementById('wb-prod-rate-3').value = 450;
            calculateWaterBalance();

            document.getElementById('sam-N').value = 2290;
            document.getElementById('sam-p').value = 0.5;
            document.getElementById('sam-e').value = 0.18;
            calculateSampling();

            document.getElementById('fin-contract-val').value = 49988000;
            document.getElementById('fin-penalty-rate').value = 0.25;
            document.getElementById('fin-delay-days').value = 7;
            document.getElementById('fin-loan-interest').value = 2.0;
            document.getElementById('fin-idle-days').value = 30;
            document.getElementById('fin-revenue').value = 1348878;
            document.getElementById('fin-expense').value = 2650658.67;
            document.getElementById('fin-vol-sold').value = 192696;
            document.getElementById('fin-tariff').value = 7.00;
            calculateFinancials();

            renderRiskMatrixTable();
            recalculateAllRiskScores();
            renderPipelineTable();

            switchTab('dashboard');

            const btn = document.getElementById('btn-load-sample');
            btn.innerHTML = `<i data-lucide="check" class="w-4 h-4"></i> โหลดข้อมูลสำเร็จแล้ว`;
            lucide.createIcons();
            setTimeout(() => {
                btn.innerHTML = `<i data-lucide="database" class="w-4 h-4"></i> <span class="hidden sm:inline">โหลดตัวอย่าง</span> <span>อบต.ไชยราช (๔๙.๙๘ ลบ.)</span>`;
                lucide.createIcons();
            }, 1800);
        }

        window.addEventListener('DOMContentLoaded', () => {
            lucide.createIcons();
            initRiskChart();
            renderActionTracker();
            calculateWaterBalance();
            calculateSampling();
            calculateFinancials();
            renderPipelineTable();
            renderRiskMatrixTable();
        });
    </script>
</body>
</html>
"""

# เรนเดอร์คอมโพเนนต์ HTML
components.html(html_code, height=1050, scrolling=True)
