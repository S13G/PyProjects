from textblob import TextBlob

file = open("text.txt", "r+")
open_file = file.read()

print("Original text: " + str(open_file))

correction = TextBlob(open_file)

corrected = correction.correct()

print("Corrected text: " + str(corrected))
file.close()

write_into = open("text.txt", "w")
write_into.write(str(corrected))
write_into.close()
