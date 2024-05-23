import math

def main() :
    with open("TP4/poème.txt", 'r', encoding="UTF-8") as f :
        current_text = f.read()

    for char in ".,!?" :
        current_text = current_text.replace(f" {char}", "")
        current_text = current_text.replace(char, "")

    current_text = current_text.replace("'", " ")
    current_text = current_text.replace("\n", " ")
    words = current_text.split(" ")


    with open("output.txt", "w") as f :
        test_pi = 0
        pwr = 0
        for word in words :
            digit = len(word) % 10
            f.write(str(digit))
            test_pi += digit * 10**pwr
            if pwr == 0 :
                f.write(".")
            pwr -= 1
            
        print(test_pi, "\n", math.pi - math.pi % 10**pwr, sep = "")
        print(f"Les deux valeurs sont elles égales : {test_pi == math.pi - math.pi % 10**pwr}")        

if __name__ == "__main__" :
    main()