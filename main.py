# -*- coding: utf-8 -*-
from selenium import webdriver
from time import sleep
from secret import password, username

WAIT = 0.2

class EcoleDBot :
    
    def __init__(self, username, pw) :
        self.username = username
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.ecoledirecte.com/login/")
        print(">>Connected to https://www.ecoledirecte.com/login/")
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        print(">>Name filled")
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pw)
        print(">>Password filled")

        self.driver.find_element_by_id('connexion').click()
        print(">>Connecting...")
        sleep(3)
        print(">>Succesfully connected !")

    def quit(self) :
    	self.driver.quit()
        
    def get_notes(self) :
        self.driver.find_element_by_class_name("icon-ed_note").click()
        print(f">>Notes's page Aquired")
        sleep(3)
        tbody = self.driver.find_element_by_tag_name("tbody")
        liste_note_box = tbody.find_elements_by_class_name("notes")
        notes = []
        for i in liste_note_box :
            x = []
            for j in i.find_elements_by_class_name('valeur') :
                x.append(j.text)
            notes.append(x)
        liste_topic_box = tbody.find_elements_by_class_name("discipline")
        topic = []
        for i in liste_topic_box :
            topic.append(i.find_element_by_class_name('nommatiere').text)
        print(f">>Page data acquiered")
        print(f">>Processing data...")
        self.show_notes(notes, topic)
        print(f">>Done !")

    def show_notes(self, notes, topic) :
        moyennes = []
        moyenne_g = 0
        coeff_g = 0
        for i in notes :
            all_coeff = 0
            all_notes = 0
            for j in i :
                next_char = False
                is_diviseur = False
                is_coef = False
                process = "note"
                n = ""
                t = str(20)
                coeff = 1
                for char in j :
                    if char == "/" :
                        is_diviseur = True
                        t = ""
                    if char == "(" :
                        is_coef = True
                        coeff = ""

                for char in j :
                    next_char = False
                    if process == "note" :
                        if char == " " :
                            if is_diviseur :
                                process = "diviseur"
                            elif is_coef :
                                process = "coef"
                            else :
                                process = None
                            next_char = True
                        else :
                            n += char

                    if process == "diviseur" and not next_char :
                        if char == " " :
                            if is_coef :
                                process = "coef"
                            else :
                                process = None
                            next_char = True
                        elif char != "/" :
                            t += char

                    if process == "coef" and not next_char:
                        if char != "(" and char != ")" :
                            coeff += char

                if n != "Disp" and n != "Abs":
                    all_notes += float(n.replace(",", "."))/float(t.replace(",", "."))*float(coeff)*20
                    all_coeff += float(coeff)

            if all_coeff == 0 :
                moyennes.append(None)
            else :
                moyennes.append(all_notes/all_coeff)
                moyenne_g += all_notes/all_coeff
                coeff_g += 1

        for i in range(len(notes)) :
        	try :
        		x = round(moyennes[i], 2)
        	except :
        		x = moyennes[i]
        	finally :
	            print(f"\n    Votre moyenne en {topic[i]} est {x}")
	            sleep(WAIT)
        print(f"\n\n    Votre moyenne générale est : {round(moyenne_g/coeff_g, 2)}\n\n")


            
        
bot = EcoleDBot(username, password)
bot.get_notes()
bot.quit()
