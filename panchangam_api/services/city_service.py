"""
Global cities database and lookup service.
Provides coordinate resolution, timezone discovery, nearest-city matching, and instant autocomplete
across hundreds of worldwide cities and sacred Hindu pilgrim centers (kshetras).
"""

import math
from typing import List, Optional, Dict

GLOBAL_CITIES = [
    # --- India: Telangana & Andhra Pradesh ---
    {"name": "Hyderabad", "state": "Telangana", "country": "India", "lat": 17.3850, "lon": 78.4867, "tz": "Asia/Kolkata"},
    {"name": "Secunderabad", "state": "Telangana", "country": "India", "lat": 17.4399, "lon": 78.4983, "tz": "Asia/Kolkata"},
    {"name": "Warangal", "state": "Telangana", "country": "India", "lat": 17.9784, "lon": 79.5941, "tz": "Asia/Kolkata"},
    {"name": "Karimnagar", "state": "Telangana", "country": "India", "lat": 18.4386, "lon": 79.1288, "tz": "Asia/Kolkata"},
    {"name": "Nizamabad", "state": "Telangana", "country": "India", "lat": 18.6725, "lon": 78.0941, "tz": "Asia/Kolkata"},
    {"name": "Khammam", "state": "Telangana", "country": "India", "lat": 17.2473, "lon": 80.1514, "tz": "Asia/Kolkata"},
    {"name": "Mahabubnagar", "state": "Telangana", "country": "India", "lat": 16.7488, "lon": 77.9856, "tz": "Asia/Kolkata"},
    {"name": "Nalgonda", "state": "Telangana", "country": "India", "lat": 17.0575, "lon": 79.2684, "tz": "Asia/Kolkata"},
    {"name": "Bhadrachalam", "state": "Telangana", "country": "India", "lat": 17.6688, "lon": 80.8936, "tz": "Asia/Kolkata"},
    {"name": "Yadagirigutta", "state": "Telangana", "country": "India", "lat": 17.5898, "lon": 78.9388, "tz": "Asia/Kolkata"},
    {"name": "Basara", "state": "Telangana", "country": "India", "lat": 18.9760, "lon": 77.9540, "tz": "Asia/Kolkata"},
    {"name": "Alampur", "state": "Telangana", "country": "India", "lat": 15.8790, "lon": 78.1360, "tz": "Asia/Kolkata"},
    {"name": "Amaravati", "state": "Andhra Pradesh", "country": "India", "lat": 16.5417, "lon": 80.5158, "tz": "Asia/Kolkata"},
    {"name": "Vijayawada", "state": "Andhra Pradesh", "country": "India", "lat": 16.5062, "lon": 80.6480, "tz": "Asia/Kolkata"},
    {"name": "Visakhapatnam", "state": "Andhra Pradesh", "country": "India", "lat": 17.6868, "lon": 83.2185, "tz": "Asia/Kolkata"},
    {"name": "Tirupati", "state": "Andhra Pradesh", "country": "India", "lat": 13.6288, "lon": 79.4192, "tz": "Asia/Kolkata"},
    {"name": "Srisailam", "state": "Andhra Pradesh", "country": "India", "lat": 16.0735, "lon": 78.8682, "tz": "Asia/Kolkata"},
    {"name": "Guntur", "state": "Andhra Pradesh", "country": "India", "lat": 16.3067, "lon": 80.4365, "tz": "Asia/Kolkata"},
    {"name": "Rajahmundry", "state": "Andhra Pradesh", "country": "India", "lat": 17.0005, "lon": 81.8040, "tz": "Asia/Kolkata"},
    {"name": "Kakinada", "state": "Andhra Pradesh", "country": "India", "lat": 16.9891, "lon": 82.2475, "tz": "Asia/Kolkata"},
    {"name": "Nellore", "state": "Andhra Pradesh", "country": "India", "lat": 14.4426, "lon": 79.9865, "tz": "Asia/Kolkata"},
    {"name": "Kurnool", "state": "Andhra Pradesh", "country": "India", "lat": 15.8281, "lon": 78.0373, "tz": "Asia/Kolkata"},
    {"name": "Kadapa", "state": "Andhra Pradesh", "country": "India", "lat": 14.4673, "lon": 78.8242, "tz": "Asia/Kolkata"},
    {"name": "Anantapur", "state": "Andhra Pradesh", "country": "India", "lat": 14.6819, "lon": 77.6006, "tz": "Asia/Kolkata"},
    {"name": "Eluru", "state": "Andhra Pradesh", "country": "India", "lat": 16.7107, "lon": 81.0952, "tz": "Asia/Kolkata"},
    {"name": "Ongole", "state": "Andhra Pradesh", "country": "India", "lat": 15.5057, "lon": 80.0499, "tz": "Asia/Kolkata"},
    {"name": "Srikakulam", "state": "Andhra Pradesh", "country": "India", "lat": 18.2949, "lon": 83.8938, "tz": "Asia/Kolkata"},
    {"name": "Vizianagaram", "state": "Andhra Pradesh", "country": "India", "lat": 18.1067, "lon": 83.3956, "tz": "Asia/Kolkata"},
    {"name": "Machilipatnam", "state": "Andhra Pradesh", "country": "India", "lat": 16.1875, "lon": 81.1389, "tz": "Asia/Kolkata"},
    {"name": "Simhachalam", "state": "Andhra Pradesh", "country": "India", "lat": 17.7663, "lon": 83.2505, "tz": "Asia/Kolkata"},
    {"name": "Draksharamam", "state": "Andhra Pradesh", "country": "India", "lat": 16.7925, "lon": 82.0628, "tz": "Asia/Kolkata"},
    {"name": "Mantralayam", "state": "Andhra Pradesh", "country": "India", "lat": 15.9400, "lon": 77.4300, "tz": "Asia/Kolkata"},
    {"name": "Ahobilam", "state": "Andhra Pradesh", "country": "India", "lat": 15.1333, "lon": 78.7167, "tz": "Asia/Kolkata"},
    {"name": "Mahanandi", "state": "Andhra Pradesh", "country": "India", "lat": 15.4800, "lon": 78.6200, "tz": "Asia/Kolkata"},

    # --- India: Tamil Nadu, Karnataka, Kerala ---
    {"name": "Bengaluru", "state": "Karnataka", "country": "India", "lat": 12.9716, "lon": 77.5946, "tz": "Asia/Kolkata"},
    {"name": "Mysuru", "state": "Karnataka", "country": "India", "lat": 12.2958, "lon": 76.6394, "tz": "Asia/Kolkata"},
    {"name": "Mangaluru", "state": "Karnataka", "country": "India", "lat": 12.9141, "lon": 74.8560, "tz": "Asia/Kolkata"},
    {"name": "Hubballi", "state": "Karnataka", "country": "India", "lat": 15.3647, "lon": 75.1240, "tz": "Asia/Kolkata"},
    {"name": "Belagavi", "state": "Karnataka", "country": "India", "lat": 15.8497, "lon": 74.4977, "tz": "Asia/Kolkata"},
    {"name": "Udupi", "state": "Karnataka", "country": "India", "lat": 13.3409, "lon": 74.7421, "tz": "Asia/Kolkata"},
    {"name": "Dharmasthala", "state": "Karnataka", "country": "India", "lat": 12.9556, "lon": 75.3800, "tz": "Asia/Kolkata"},
    {"name": "Sringeri", "state": "Karnataka", "country": "India", "lat": 13.4189, "lon": 75.2570, "tz": "Asia/Kolkata"},
    {"name": "Gokarna", "state": "Karnataka", "country": "India", "lat": 14.5426, "lon": 74.3188, "tz": "Asia/Kolkata"},
    {"name": "Kukke Subramanya", "state": "Karnataka", "country": "India", "lat": 12.6667, "lon": 75.6167, "tz": "Asia/Kolkata"},
    {"name": "Chennai", "state": "Tamil Nadu", "country": "India", "lat": 13.0827, "lon": 80.2707, "tz": "Asia/Kolkata"},
    {"name": "Coimbatore", "state": "Tamil Nadu", "country": "India", "lat": 11.0168, "lon": 76.9558, "tz": "Asia/Kolkata"},
    {"name": "Madurai", "state": "Tamil Nadu", "country": "India", "lat": 9.9252, "lon": 78.1198, "tz": "Asia/Kolkata"},
    {"name": "Tiruchirappalli", "state": "Tamil Nadu", "country": "India", "lat": 10.7905, "lon": 78.7047, "tz": "Asia/Kolkata"},
    {"name": "Salem", "state": "Tamil Nadu", "country": "India", "lat": 11.6643, "lon": 78.1460, "tz": "Asia/Kolkata"},
    {"name": "Kanchipuram", "state": "Tamil Nadu", "country": "India", "lat": 12.8342, "lon": 79.7036, "tz": "Asia/Kolkata"},
    {"name": "Rameswaram", "state": "Tamil Nadu", "country": "India", "lat": 9.2876, "lon": 79.3129, "tz": "Asia/Kolkata"},
    {"name": "Chidambaram", "state": "Tamil Nadu", "country": "India", "lat": 11.3992, "lon": 79.6936, "tz": "Asia/Kolkata"},
    {"name": "Tiruvannamalai", "state": "Tamil Nadu", "country": "India", "lat": 12.2253, "lon": 79.0747, "tz": "Asia/Kolkata"},
    {"name": "Thanjavur", "state": "Tamil Nadu", "country": "India", "lat": 10.7870, "lon": 79.1378, "tz": "Asia/Kolkata"},
    {"name": "Palani", "state": "Tamil Nadu", "country": "India", "lat": 10.4500, "lon": 77.5167, "tz": "Asia/Kolkata"},
    {"name": "Kanyakumari", "state": "Tamil Nadu", "country": "India", "lat": 8.0883, "lon": 77.5385, "tz": "Asia/Kolkata"},
    {"name": "Kochi", "state": "Kerala", "country": "India", "lat": 9.9312, "lon": 76.2673, "tz": "Asia/Kolkata"},
    {"name": "Thiruvananthapuram", "state": "Kerala", "country": "India", "lat": 8.5241, "lon": 76.9366, "tz": "Asia/Kolkata"},
    {"name": "Kozhikode", "state": "Kerala", "country": "India", "lat": 11.2588, "lon": 75.7804, "tz": "Asia/Kolkata"},
    {"name": "Thrissur", "state": "Kerala", "country": "India", "lat": 10.5276, "lon": 76.2144, "tz": "Asia/Kolkata"},
    {"name": "Guruvayur", "state": "Kerala", "country": "India", "lat": 10.5946, "lon": 76.0400, "tz": "Asia/Kolkata"},
    {"name": "Sabarimala", "state": "Kerala", "country": "India", "lat": 9.4406, "lon": 77.0811, "tz": "Asia/Kolkata"},

    # --- India: Maharashtra, Gujarat, Central & North ---
    {"name": "Mumbai", "state": "Maharashtra", "country": "India", "lat": 19.0760, "lon": 72.8777, "tz": "Asia/Kolkata"},
    {"name": "Pune", "state": "Maharashtra", "country": "India", "lat": 18.5204, "lon": 73.8567, "tz": "Asia/Kolkata"},
    {"name": "Nagpur", "state": "Maharashtra", "country": "India", "lat": 21.1458, "lon": 79.0882, "tz": "Asia/Kolkata"},
    {"name": "Nashik", "state": "Maharashtra", "country": "India", "lat": 19.9975, "lon": 73.7898, "tz": "Asia/Kolkata"},
    {"name": "Shirdi", "state": "Maharashtra", "country": "India", "lat": 19.7667, "lon": 74.4764, "tz": "Asia/Kolkata"},
    {"name": "Trimbakeshwar", "state": "Maharashtra", "country": "India", "lat": 19.9325, "lon": 73.5303, "tz": "Asia/Kolkata"},
    {"name": "Pandharpur", "state": "Maharashtra", "country": "India", "lat": 17.6778, "lon": 75.3267, "tz": "Asia/Kolkata"},
    {"name": "Kolhapur", "state": "Maharashtra", "country": "India", "lat": 16.7050, "lon": 74.2433, "tz": "Asia/Kolkata"},
    {"name": "Ahmedabad", "state": "Gujarat", "country": "India", "lat": 23.0225, "lon": 72.5714, "tz": "Asia/Kolkata"},
    {"name": "Surat", "state": "Gujarat", "country": "India", "lat": 21.1702, "lon": 72.8311, "tz": "Asia/Kolkata"},
    {"name": "Vadodara", "state": "Gujarat", "country": "India", "lat": 22.3072, "lon": 73.1812, "tz": "Asia/Kolkata"},
    {"name": "Rajkot", "state": "Gujarat", "country": "India", "lat": 22.3039, "lon": 70.8022, "tz": "Asia/Kolkata"},
    {"name": "Somnath", "state": "Gujarat", "country": "India", "lat": 20.8880, "lon": 70.4010, "tz": "Asia/Kolkata"},
    {"name": "Dwarka", "state": "Gujarat", "country": "India", "lat": 22.2442, "lon": 68.9685, "tz": "Asia/Kolkata"},
    {"name": "New Delhi", "state": "Delhi", "country": "India", "lat": 28.6139, "lon": 77.2090, "tz": "Asia/Kolkata"},
    {"name": "Noida", "state": "Uttar Pradesh", "country": "India", "lat": 28.5355, "lon": 77.3910, "tz": "Asia/Kolkata"},
    {"name": "Gurugram", "state": "Haryana", "country": "India", "lat": 28.4595, "lon": 77.0266, "tz": "Asia/Kolkata"},
    {"name": "Varanasi (Kashi)", "state": "Uttar Pradesh", "country": "India", "lat": 25.3176, "lon": 82.9739, "tz": "Asia/Kolkata"},
    {"name": "Ayodhya", "state": "Uttar Pradesh", "country": "India", "lat": 26.7922, "lon": 82.1998, "tz": "Asia/Kolkata"},
    {"name": "Prayagraj", "state": "Uttar Pradesh", "country": "India", "lat": 25.4358, "lon": 81.8463, "tz": "Asia/Kolkata"},
    {"name": "Mathura", "state": "Uttar Pradesh", "country": "India", "lat": 27.4924, "lon": 77.6737, "tz": "Asia/Kolkata"},
    {"name": "Vrindavan", "state": "Uttar Pradesh", "country": "India", "lat": 27.5828, "lon": 77.7006, "tz": "Asia/Kolkata"},
    {"name": "Haridwar", "state": "Uttarakhand", "country": "India", "lat": 29.9457, "lon": 78.1642, "tz": "Asia/Kolkata"},
    {"name": "Rishikesh", "state": "Uttarakhand", "country": "India", "lat": 30.0869, "lon": 78.2676, "tz": "Asia/Kolkata"},
    {"name": "Badrinath", "state": "Uttarakhand", "country": "India", "lat": 30.7433, "lon": 79.4938, "tz": "Asia/Kolkata"},
    {"name": "Kedarnath", "state": "Uttarakhand", "country": "India", "lat": 30.7352, "lon": 79.0669, "tz": "Asia/Kolkata"},
    {"name": "Jaipur", "state": "Rajasthan", "country": "India", "lat": 26.9124, "lon": 75.7873, "tz": "Asia/Kolkata"},
    {"name": "Udaipur", "state": "Rajasthan", "country": "India", "lat": 24.5854, "lon": 73.7125, "tz": "Asia/Kolkata"},
    {"name": "Ujjain", "state": "Madhya Pradesh", "country": "India", "lat": 23.1765, "lon": 75.7885, "tz": "Asia/Kolkata"},
    {"name": "Indore", "state": "Madhya Pradesh", "country": "India", "lat": 22.7196, "lon": 75.8577, "tz": "Asia/Kolkata"},
    {"name": "Bhopal", "state": "Madhya Pradesh", "country": "India", "lat": 23.2599, "lon": 77.4126, "tz": "Asia/Kolkata"},
    {"name": "Puri", "state": "Odisha", "country": "India", "lat": 19.8135, "lon": 85.8312, "tz": "Asia/Kolkata"},
    {"name": "Bhubaneswar", "state": "Odisha", "country": "India", "lat": 20.2961, "lon": 85.8245, "tz": "Asia/Kolkata"},
    {"name": "Kolkata", "state": "West Bengal", "country": "India", "lat": 22.5726, "lon": 88.3639, "tz": "Asia/Kolkata"},
    {"name": "Patna", "state": "Bihar", "country": "India", "lat": 25.5941, "lon": 85.1376, "tz": "Asia/Kolkata"},
    {"name": "Gaya", "state": "Bihar", "country": "India", "lat": 24.7914, "lon": 85.0002, "tz": "Asia/Kolkata"},
    {"name": "Guwahati", "state": "Assam", "country": "India", "lat": 26.1445, "lon": 91.7362, "tz": "Asia/Kolkata"},
    {"name": "Chandigarh", "state": "Punjab/Haryana", "country": "India", "lat": 30.7333, "lon": 76.7794, "tz": "Asia/Kolkata"},
    {"name": "Amritsar", "state": "Punjab", "country": "India", "lat": 31.6340, "lon": 74.8723, "tz": "Asia/Kolkata"},

    # --- USA: Texas & South ---
    {"name": "Frisco", "state": "Texas", "country": "USA", "lat": 33.1507, "lon": -96.8236, "tz": "America/Chicago"},
    {"name": "Dallas", "state": "Texas", "country": "USA", "lat": 32.7767, "lon": -96.7970, "tz": "America/Chicago"},
    {"name": "Plano", "state": "Texas", "country": "USA", "lat": 33.0198, "lon": -96.6989, "tz": "America/Chicago"},
    {"name": "Irving", "state": "Texas", "country": "USA", "lat": 32.8140, "lon": -96.9489, "tz": "America/Chicago"},
    {"name": "Austin", "state": "Texas", "country": "USA", "lat": 30.2672, "lon": -97.7431, "tz": "America/Chicago"},
    {"name": "Houston", "state": "Texas", "country": "USA", "lat": 29.7604, "lon": -95.3698, "tz": "America/Chicago"},
    {"name": "San Antonio", "state": "Texas", "country": "USA", "lat": 29.4241, "lon": -98.4936, "tz": "America/Chicago"},
    {"name": "Fort Worth", "state": "Texas", "country": "USA", "lat": 32.7555, "lon": -97.3308, "tz": "America/Chicago"},
    {"name": "Round Rock", "state": "Texas", "country": "USA", "lat": 30.5083, "lon": -97.6789, "tz": "America/Chicago"},
    {"name": "Sugar Land", "state": "Texas", "country": "USA", "lat": 29.6197, "lon": -95.6349, "tz": "America/Chicago"},
    {"name": "McKinney", "state": "Texas", "country": "USA", "lat": 33.1972, "lon": -96.6397, "tz": "America/Chicago"},

    # --- USA: California & West ---
    {"name": "San Jose", "state": "California", "country": "USA", "lat": 37.3382, "lon": -121.8863, "tz": "America/Los_Angeles"},
    {"name": "San Francisco", "state": "California", "country": "USA", "lat": 37.7749, "lon": -122.4194, "tz": "America/Los_Angeles"},
    {"name": "Fremont", "state": "California", "country": "USA", "lat": 37.5485, "lon": -121.9886, "tz": "America/Los_Angeles"},
    {"name": "Sunnyvale", "state": "California", "country": "USA", "lat": 37.3688, "lon": -122.0363, "tz": "America/Los_Angeles"},
    {"name": "Santa Clara", "state": "California", "country": "USA", "lat": 37.3541, "lon": -121.9552, "tz": "America/Los_Angeles"},
    {"name": "Los Angeles", "state": "California", "country": "USA", "lat": 34.0522, "lon": -118.2437, "tz": "America/Los_Angeles"},
    {"name": "San Diego", "state": "California", "country": "USA", "lat": 32.7157, "lon": -117.1611, "tz": "America/Los_Angeles"},
    {"name": "Irvine", "state": "California", "country": "USA", "lat": 33.6846, "lon": -117.8265, "tz": "America/Los_Angeles"},
    {"name": "Pleasanton", "state": "California", "country": "USA", "lat": 37.6624, "lon": -121.8747, "tz": "America/Los_Angeles"},
    {"name": "Sacramento", "state": "California", "country": "USA", "lat": 38.5816, "lon": -121.4944, "tz": "America/Los_Angeles"},
    {"name": "Seattle", "state": "Washington", "country": "USA", "lat": 47.6062, "lon": -122.3321, "tz": "America/Los_Angeles"},
    {"name": "Bellevue", "state": "Washington", "country": "USA", "lat": 47.6101, "lon": -122.2015, "tz": "America/Los_Angeles"},
    {"name": "Redmond", "state": "Washington", "country": "USA", "lat": 47.6740, "lon": -122.1215, "tz": "America/Los_Angeles"},
    {"name": "Portland", "state": "Oregon", "country": "USA", "lat": 45.5152, "lon": -122.6784, "tz": "America/Los_Angeles"},
    {"name": "Beaverton", "state": "Oregon", "country": "USA", "lat": 45.4871, "lon": -122.8037, "tz": "America/Los_Angeles"},
    {"name": "Phoenix", "state": "Arizona", "country": "USA", "lat": 33.4484, "lon": -112.0740, "tz": "America/Phoenix"},
    {"name": "Chandler", "state": "Arizona", "country": "USA", "lat": 33.3062, "lon": -111.8413, "tz": "America/Phoenix"},
    {"name": "Denver", "state": "Colorado", "country": "USA", "lat": 39.7392, "lon": -104.9903, "tz": "America/Denver"},
    {"name": "Salt Lake City", "state": "Utah", "country": "USA", "lat": 40.7608, "lon": -111.8910, "tz": "America/Denver"},
    {"name": "Las Vegas", "state": "Nevada", "country": "USA", "lat": 36.1699, "lon": -115.1398, "tz": "America/Los_Angeles"},

    # --- USA: Midwest, East Coast & South ---
    {"name": "Chicago", "state": "Illinois", "country": "USA", "lat": 41.8781, "lon": -87.6298, "tz": "America/Chicago"},
    {"name": "Naperville", "state": "Illinois", "country": "USA", "lat": 41.7508, "lon": -88.1535, "tz": "America/Chicago"},
    {"name": "Schaumburg", "state": "Illinois", "country": "USA", "lat": 42.0334, "lon": -88.0834, "tz": "America/Chicago"},
    {"name": "New York", "state": "New York", "country": "USA", "lat": 40.7128, "lon": -74.0060, "tz": "America/New_York"},
    {"name": "Edison", "state": "New Jersey", "country": "USA", "lat": 40.5187, "lon": -74.4121, "tz": "America/New_York"},
    {"name": "Jersey City", "state": "New Jersey", "country": "USA", "lat": 40.7178, "lon": -74.0431, "tz": "America/New_York"},
    {"name": "Princeton", "state": "New Jersey", "country": "USA", "lat": 40.3573, "lon": -74.6672, "tz": "America/New_York"},
    {"name": "Atlanta", "state": "Georgia", "country": "USA", "lat": 33.7490, "lon": -84.3880, "tz": "America/New_York"},
    {"name": "Alpharetta", "state": "Georgia", "country": "USA", "lat": 34.0754, "lon": -84.2941, "tz": "America/New_York"},
    {"name": "Cumming", "state": "Georgia", "country": "USA", "lat": 34.2073, "lon": -84.1402, "tz": "America/New_York"},
    {"name": "Charlotte", "state": "North Carolina", "country": "USA", "lat": 35.2271, "lon": -80.8431, "tz": "America/New_York"},
    {"name": "Raleigh", "state": "North Carolina", "country": "USA", "lat": 35.7796, "lon": -78.6382, "tz": "America/New_York"},
    {"name": "Cary", "state": "North Carolina", "country": "USA", "lat": 35.7915, "lon": -78.7811, "tz": "America/New_York"},
    {"name": "Boston", "state": "Massachusetts", "country": "USA", "lat": 42.3601, "lon": -71.0589, "tz": "America/New_York"},
    {"name": "Washington DC", "state": "District of Columbia", "country": "USA", "lat": 38.9072, "lon": -77.0369, "tz": "America/New_York"},
    {"name": "Ashburn", "state": "Virginia", "country": "USA", "lat": 39.0438, "lon": -77.4874, "tz": "America/New_York"},
    {"name": "Detroit", "state": "Michigan", "country": "USA", "lat": 42.3314, "lon": -83.0458, "tz": "America/New_York"},
    {"name": "Troy", "state": "Michigan", "country": "USA", "lat": 42.6064, "lon": -83.1498, "tz": "America/New_York"},
    {"name": "Columbus", "state": "Ohio", "country": "USA", "lat": 39.9612, "lon": -82.9988, "tz": "America/New_York"},
    {"name": "Cincinnati", "state": "Ohio", "country": "USA", "lat": 39.1031, "lon": -84.5120, "tz": "America/New_York"},
    {"name": "Philadelphia", "state": "Pennsylvania", "country": "USA", "lat": 39.9526, "lon": -75.1652, "tz": "America/New_York"},
    {"name": "Pittsburgh", "state": "Pennsylvania", "country": "USA", "lat": 40.4406, "lon": -79.9959, "tz": "America/New_York"},
    {"name": "Tampa", "state": "Florida", "country": "USA", "lat": 27.9506, "lon": -82.4572, "tz": "America/New_York"},
    {"name": "Orlando", "state": "Florida", "country": "USA", "lat": 28.5383, "lon": -81.3792, "tz": "America/New_York"},
    {"name": "Miami", "state": "Florida", "country": "USA", "lat": 25.7617, "lon": -80.1918, "tz": "America/New_York"},
    {"name": "Minneapolis", "state": "Minnesota", "country": "USA", "lat": 44.9778, "lon": -93.2650, "tz": "America/Chicago"},
    {"name": "St. Louis", "state": "Missouri", "country": "USA", "lat": 38.6270, "lon": -90.1994, "tz": "America/Chicago"},
    {"name": "Nashville", "state": "Tennessee", "country": "USA", "lat": 36.1627, "lon": -86.7816, "tz": "America/Chicago"},

    # --- Canada ---
    {"name": "Toronto", "state": "Ontario", "country": "Canada", "lat": 43.6532, "lon": -79.3832, "tz": "America/Toronto"},
    {"name": "Brampton", "state": "Ontario", "country": "Canada", "lat": 43.7315, "lon": -79.7624, "tz": "America/Toronto"},
    {"name": "Mississauga", "state": "Ontario", "country": "Canada", "lat": 43.5890, "lon": -79.6441, "tz": "America/Toronto"},
    {"name": "Vancouver", "state": "British Columbia", "country": "Canada", "lat": 49.2827, "lon": -123.1207, "tz": "America/Vancouver"},
    {"name": "Surrey", "state": "British Columbia", "country": "Canada", "lat": 49.1913, "lon": -122.8490, "tz": "America/Vancouver"},
    {"name": "Calgary", "state": "Alberta", "country": "Canada", "lat": 51.0447, "lon": -114.0719, "tz": "America/Edmonton"},
    {"name": "Edmonton", "state": "Alberta", "country": "Canada", "lat": 53.5461, "lon": -113.4938, "tz": "America/Edmonton"},
    {"name": "Ottawa", "state": "Ontario", "country": "Canada", "lat": 45.4215, "lon": -75.6972, "tz": "America/Toronto"},
    {"name": "Montreal", "state": "Quebec", "country": "Canada", "lat": 45.5017, "lon": -73.5673, "tz": "America/Toronto"},

    # --- UK & Europe ---
    {"name": "London", "state": "England", "country": "UK", "lat": 51.5074, "lon": -0.1278, "tz": "Europe/London"},
    {"name": "Leicester", "state": "England", "country": "UK", "lat": 52.6369, "lon": -1.1398, "tz": "Europe/London"},
    {"name": "Birmingham", "state": "England", "country": "UK", "lat": 52.4862, "lon": -1.8904, "tz": "Europe/London"},
    {"name": "Manchester", "state": "England", "country": "UK", "lat": 53.4808, "lon": -2.2426, "tz": "Europe/London"},
    {"name": "Leeds", "state": "England", "country": "UK", "lat": 53.8008, "lon": -1.5491, "tz": "Europe/London"},
    {"name": "Edinburgh", "state": "Scotland", "country": "UK", "lat": 55.9533, "lon": -3.1883, "tz": "Europe/London"},
    {"name": "Dublin", "state": "Leinster", "country": "Ireland", "lat": 53.3498, "lon": -6.2603, "tz": "Europe/Dublin"},
    {"name": "Paris", "state": "Île-de-France", "country": "France", "lat": 48.8566, "lon": 2.3522, "tz": "Europe/Paris"},
    {"name": "Berlin", "state": "Berlin", "country": "Germany", "lat": 52.5200, "lon": 13.4050, "tz": "Europe/Berlin"},
    {"name": "Frankfurt", "state": "Hesse", "country": "Germany", "lat": 50.1109, "lon": 8.6821, "tz": "Europe/Berlin"},
    {"name": "Munich", "state": "Bavaria", "country": "Germany", "lat": 48.1351, "lon": 11.5820, "tz": "Europe/Berlin"},
    {"name": "Amsterdam", "state": "North Holland", "country": "Netherlands", "lat": 52.3676, "lon": 4.9041, "tz": "Europe/Amsterdam"},
    {"name": "Zurich", "state": "Zurich", "country": "Switzerland", "lat": 47.3769, "lon": 8.5417, "tz": "Europe/Zurich"},
    {"name": "Geneva", "state": "Geneva", "country": "Switzerland", "lat": 46.2044, "lon": 6.1432, "tz": "Europe/Zurich"},
    {"name": "Rome", "state": "Lazio", "country": "Italy", "lat": 41.9028, "lon": 12.4964, "tz": "Europe/Rome"},
    {"name": "Stockholm", "state": "Stockholm", "country": "Sweden", "lat": 59.3293, "lon": 18.0686, "tz": "Europe/Stockholm"},

    # --- Middle East & Gulf ---
    {"name": "Dubai", "state": "Dubai", "country": "UAE", "lat": 25.2048, "lon": 55.2708, "tz": "Asia/Dubai"},
    {"name": "Abu Dhabi", "state": "Abu Dhabi", "country": "UAE", "lat": 24.4539, "lon": 54.3773, "tz": "Asia/Dubai"},
    {"name": "Sharjah", "state": "Sharjah", "country": "UAE", "lat": 25.3463, "lon": 55.4209, "tz": "Asia/Dubai"},
    {"name": "Doha", "state": "Ad Dawhah", "country": "Qatar", "lat": 25.2854, "lon": 51.5310, "tz": "Asia/Qatar"},
    {"name": "Muscat", "state": "Muscat", "country": "Oman", "lat": 23.5859, "lon": 58.4059, "tz": "Asia/Muscat"},
    {"name": "Kuwait City", "state": "Al Asimah", "country": "Kuwait", "lat": 29.3759, "lon": 47.9774, "tz": "Asia/Kuwait"},
    {"name": "Manama", "state": "Capital", "country": "Bahrain", "lat": 26.2285, "lon": 50.5860, "tz": "Asia/Bahrain"},
    {"name": "Riyadh", "state": "Riyadh", "country": "Saudi Arabia", "lat": 24.7136, "lon": 46.6753, "tz": "Asia/Riyadh"},

    # --- Asia-Pacific, Australia & New Zealand ---
    {"name": "Singapore", "state": "Central", "country": "Singapore", "lat": 1.3521, "lon": 103.8198, "tz": "Asia/Singapore"},
    {"name": "Kuala Lumpur", "state": "Federal Territory", "country": "Malaysia", "lat": 3.1390, "lon": 101.6869, "tz": "Asia/Kuala_Lumpur"},
    {"name": "George Town", "state": "Penang", "country": "Malaysia", "lat": 5.4141, "lon": 100.3288, "tz": "Asia/Kuala_Lumpur"},
    {"name": "Bangkok", "state": "Bangkok", "country": "Thailand", "lat": 13.7563, "lon": 100.5018, "tz": "Asia/Bangkok"},
    {"name": "Tokyo", "state": "Tokyo", "country": "Japan", "lat": 35.6762, "lon": 139.6503, "tz": "Asia/Tokyo"},
    {"name": "Sydney", "state": "New South Wales", "country": "Australia", "lat": -33.8688, "lon": 151.2093, "tz": "Australia/Sydney"},
    {"name": "Melbourne", "state": "Victoria", "country": "Australia", "lat": -37.8136, "lon": 144.9631, "tz": "Australia/Melbourne"},
    {"name": "Brisbane", "state": "Queensland", "country": "Australia", "lat": -27.4698, "lon": 153.0251, "tz": "Australia/Brisbane"},
    {"name": "Perth", "state": "Western Australia", "country": "Australia", "lat": -31.9505, "lon": 115.8605, "tz": "Australia/Perth"},
    {"name": "Adelaide", "state": "South Australia", "country": "Australia", "lat": -34.9285, "lon": 138.6007, "tz": "Australia/Adelaide"},
    {"name": "Auckland", "state": "Auckland", "country": "New Zealand", "lat": -36.8485, "lon": 174.7633, "tz": "Pacific/Auckland"},
    {"name": "Wellington", "state": "Wellington", "country": "New Zealand", "lat": -41.2865, "lon": 174.7762, "tz": "Pacific/Auckland"},
    {"name": "Port Louis", "state": "Port Louis", "country": "Mauritius", "lat": -20.1609, "lon": 57.5012, "tz": "Indian/Mauritius"},
    {"name": "Suva", "state": "Central", "country": "Fiji", "lat": -18.1248, "lon": 178.4501, "tz": "Pacific/Fiji"}
]


def search_cities(query: str, limit: int = 15) -> List[Dict]:
    """Instant fuzzy / substring search across worldwide cities."""
    if not query:
        return GLOBAL_CITIES[:limit]
    
    q = query.lower().strip()
    matches = []
    
    for c in GLOBAL_CITIES:
        full_label = f"{c['name']} {c.get('state', '')} {c['country']}".lower()
        if c['name'].lower() == q:
            matches.append((-2, c))
        elif c['name'].lower().startswith(q):
            matches.append((-1, c))
        elif q in full_label:
            matches.append((1, c))
            
    matches.sort(key=lambda x: x[0])
    return [m[1] for m in matches[:limit]]


def get_city_by_name(city_name: str) -> Optional[Dict]:
    """Retrieve city entry by exact or case-insensitive match."""
    if not city_name:
        return None
    cn = city_name.lower().strip()
    for c in GLOBAL_CITIES:
        if c['name'].lower() == cn:
            return c
    return None


def find_nearest_city(lat: float, lon: float) -> Dict:
    """
    Finds closest known city in catalog using approximate Euclidean distance.
    Useful for GPS Auto-detection fallback.
    """
    best_dist = float('inf')
    best_city = GLOBAL_CITIES[0]
    
    for c in GLOBAL_CITIES:
        dist = math.hypot(c['lat'] - lat, c['lon'] - lon)
        if dist < best_dist:
            best_dist = dist
            best_city = c
            
    return best_city
