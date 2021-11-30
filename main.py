import configparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

#test
name = 'nguyen huu hieu'
phone = '0946127555'
ccnd = '186822539'

checkotp_url = 'https://tiemchungcovid19.moh.gov.vn/Account/CheckOtp'
success_otp_url = 'https://tiemchungcovid19.moh.gov.vn/KeHoachTiemChungArea/KeHoachTiem'
doituong_url = 'https://tiemchungcovid19.moh.gov.vn/TiemChung/DoiTuong/IndexCovid'

# Thông tin đăng nhập
config = configparser.RawConfigParser()   
configFilePath = r'ini.conf'
config.read(configFilePath)
username = config['ACCOUNT']['User']
password = config['ACCOUNT']['Password']

driver = webdriver.Firefox()
driver.get("https://tiemchungcovid19.moh.gov.vn/Account/Login")


# Đăng nhập và check OTP
input_username = driver.find_element_by_id('username')
input_password = driver.find_element_by_id('password')
btn_login = driver.find_element_by_id('btnLogin')

input_username.send_keys(username)
input_password.send_keys(password)
btn_login.click()

time.sleep(3)

# Kiểm tra đăng nhập thành công
is_login_success = False
current_url = driver.current_url

if current_url == checkotp_url:
    is_login_success = True 

if is_login_success:
    
    is_otp_validate = False
    while not is_otp_validate:
        otp = input("Nhập OTP: ")
        input_otp = driver.find_element_by_id('otpTxt')
        input_otp.send_keys(otp)
        btn_validateotp = driver.find_element_by_xpath('/html/body/div/div/div/div/button[1]')
        btn_validateotp.click()
        current_url = driver.current_url
        if current_url == success_otp_url:
            is_otp_validate = True
    print('Đăng nhập thành công')

    time.sleep(1)
    driver.get(doituong_url)
    time.sleep(1)

    driver.find_element_by_xpath('/html/body/section/div[2]/div[3]/div[1]/div[1]/div/div[1]/table/tbody/tr/td[2]/button').click()
    driver.find_element_by_xpath('//*[@id="select2-slDonViTao-container"]/span').click()

    input_search_name = driver.find_element_by_id('txtHoTenSearch')
    input_search_phone = driver.find_element_by_id('txtSoDienThoaiSearch')
    btn_search = driver.find_element_by_id('btnAdvancedSearch')

    input_search_name.send_keys(name)
    input_search_phone.send_keys(phone)
    btn_search.click()
    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="AdvancedSearchPopover"]/h3/span').click()
    driver.find_element_by_xpath('//*[@id="doiTuongSearchResult"]/tbody/tr/td[2]/div').click()
    time.sleep(2)

    driver.find_element_by_id('btnEdit').click()
   
    time.sleep(3)
    quocgia = driver.find_element_by_id('select2-slQuocGia_Sua-container')
    quocgia.click()
    input_quocgia = driver.find_element_by_xpath('/html/body/span/span/span[1]/input')
    input_quocgia.send_keys('Việt Nam')
    time.sleep(1)
    input_quocgia.send_keys(Keys.RETURN)

    input_cmnd = driver.find_element_by_id('txtCMT_Sua')
    old_cmnd = input_cmnd.get_attribute('value')
    input_cmnd.clear()
    input_cmnd.send_keys(ccnd)
    time.sleep(1)

    driver.find_element_by_id('btnSave').click()
    time.sleep(2)

    print('Cập nhật thành công đối tượng:', name,'.', old_cmnd, '-->' , ccnd )

else:
    print("Sai tên đăng nhập hoặc mật khẩu, vui lòng kiểm tra lại thông tin trong file ini.conf")