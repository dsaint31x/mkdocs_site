def print_ascii():
    
    for code in range(33,128):
        if code != 127 : # DEL
            print(f"{code:04} | {code:<#07b} | { chr(code)}")
        else:
            print(f"{code:04} | {bin(code):07} | DEL")
            
if __name__ == "__main__":
    print_ascii()