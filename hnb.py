import random as rnd
import collections as collect

#COMP3005
#Vishesh Saharan
#HW7

def load_words(filename,length):
    try:
        with open(filename) as f:
            words=[]
            for line in f:
                if len(line.strip())==length:
                    words.append(line.strip().lower())
            return words
    except FileNotFoundError:
        print("File Not Found")
        return []


def game_over(guesses_remaining,hint):
    """Determines if a game has been played out 

    Args:
        guesses_remaining (int): Number of guesses remaining 
        hint (str): The hint revealed to the player in the game

    Returns:
        boolean: True if the guesses have hit 0 or there are no more dashes in 
                the hint. Returns False for everything else 
    """ 
    if guesses_remaining<=0:
        return True
    if hint.count("-")==0:
        return True 
    return False 


def test_game_over():
    """Tests the game_over function over 5 tests

    Args:
        None: We will call game_over function later

    Returns:
        String: We will get an error message indicating that something is wrong with the game_over function
    """
    if game_over(3,'----')!= False:
        print("Error with game_over(3,'----') function")
    if game_over(1,'coy')!= True:
        print("Error with game_over(1,'coy') function")
    if game_over(0,'--d-f')!= True:
        print("Error with game_over(0,'--d-f') function")
    if game_over(2,'sew-')!=False:
        print("Error with game_over(2,'sew-') function")
    if game_over(10,'se')!=True:
        print("Error with game_over(10,'se-') function")


def mask_word(word, guessed):
    """Returns word with all letters not in guessed replaced with hyphens

    Args:
        word (str): the word to mask
        guessed (set): the guessed letters

    Returns:
        str: the masked word
    """ 
    for i in word:
            if i in guessed:
                continue
            else:
                word=word.replace(i,"-")

    return word


def test_mask_word():
    """Tests the mask_word function over 5 tests

    Args:
        None: We will call mask_word function later

    Returns:
        String: We will get an error message indicating that something is wrong with the mask_word function
    """
    if mask_word('Freedom',{'F'})!='F------':
        print("Error with mask_word('Freedom',{'F'}) function")
    if mask_word('Freedom',{'f'})!='-------':
        print("Error with mask_word('Freedom',{'f'}) function")
    if mask_word('colorado',{'n','b','v','o','d'})!='-o-o--do':
        print("Error with mask_word('colorado',{'n','b','v','o','d'}) function")
    if mask_word('all',{'z','l','a','w'})!='all':
        print("Error with mask_word('all',{'z','l','a','w'}) function")
    if mask_word('wave',{'e','i','x','w','v'})!='w-ve':
        print("Error with mask_word('wave',{'e','i','x','w','v'}) function")


def partition(words, guessed):
    """Generates the partitions of the set words based upon guessed

    Args:
        words (set): the word set
        guessed (set): the guessed letters

    Returns:
        dict: The partitions
    """

    Part_Dict={}
    wordset4=set()
    wordset5=set()
    for i in guessed:
        for j in words:
            #If words are in guess, we will add to a wordset
            if i in j: 
                wordset4.add(j)
    
    #We then want to create a wordset without the ones we just added 
    wordset5=words-wordset4

    #This will create a new initalized value the first time a key is used. This avoids the KeyError as there 
    #is a default value provided for nonexistent keys 
    Part_Dict=collect.defaultdict(list)
    for word in words:
        #Calling on mask_word to create keys
        hint=mask_word(word,guessed)
        #We add the hints as keys and the words as values to the dictionary Part_Dict
        Part_Dict[hint].append(word)
    
    #Setting it to a dictionary after the loop and returning it 
    Part_Dict=dict(Part_Dict)
    Part_Dict={key: set(value) for key, value in Part_Dict.items()}

    return Part_Dict


def test_partition():
    """Tests the partition function over 5 tests

    Args:
        None: We will call the partition function later

    Returns:
        String: We will get an error message indicating that something is wrong with the partition function
    """
    if partition({'fly','fry'},{'y'})!={'--y': {'fly','fry'}}:
        print("Error with partition({'fly','fry','sly'},{'y'}) function")
    if partition({'wavy', 'onyx', 'waxy'},{'e','i','x'})!={'--x-': {'waxy'}, '---x': {'onyx'}, '----': {'wavy'}}:
        print("Error with partition({'wavy', 'onyx', 'waxy'},{'e','i','x'}) function ")
    if partition({'kind','bine','jive','mint'},{'n','i','e'})!={'-in-': {'kind', 'mint'}, '-ine': {'bine'}, 
    '-i-e': {'jive'}}:
        print("Error with partition({'kind','bine','jive','mint'},{'n','i','e'}) function")
    if partition({'ivy'},{'i','g'})!={'i--': {'ivy'}}:
        print("Error with partition({'ivy'},{'i','g'}) function")
    if partition({'clio','novi','alma','standish'},{'z','w','k'})!={'----': {'alma', 'clio', 'novi'}, 
    '--------': {'standish'}}:
        print("Error with partition({'clio','novi','alma','standish'},{'z','w','k'}) function")


def max_partition(partitions):
    """Returns the hint for the largest partite set

    The maximum partite set is selected by selecting the partite set with
    1. The maximum size partite set
    2. If more than one maximum, prefer the hint with fewer revealed letters
    3. If there is still a tie, select randomly

    Args:
        partitions (dict): partitions from partition function

    Returns:
        str: hint for the largest partite set

    """
    max1=0
    #Going through keys and values of dict partitions
    for i,j in partitions.items():
        count1=0
        count2=0
        #Declaring a max partite set to be based on size of set
        if (len(j))>max1:
            max1=(len(j))
            key=i
            continue
        #For the values of the max partite set, we will count the number of alphabet letters in 
        #the keys and the number of alphabet letters in the values
        if (len(j))==max1:
            for k in key:
                if k.isalpha():
                    count1+=1
            for k in i:
                if k.isalpha():
                    count2+=1
            #If the number of letters is more than keys, let's leave it alone as that 
            #is most likely going to be max partitie key 
            if count2>count1:
                pass
            #If more letters in key, then the key becomes max paritie key. This allows us to return when 
            #a correct letter has been guesses and the user can then build off that

            elif count1>count2:
                key=i
            #In the event of a tie, a random key will be chosen
            elif count1==count2:
                key=rnd.choice([i,key])
    
    return key


def test_max_partition():
    """Tests the max_partition function over 6 tests

    Args:
        None: We will call max_partition function later

    Returns:
        String: We will get an error message indicating that something is wrong with the max_parititon function
    """
    if max_partition({'-in-': {'kind', 'mint'}, '-ine': {'bine'},'-i-e': {'jive'}})!='-in-':
        print(f"Error with max_partition({'-in-': {'kind', 'mint'}, '-ine': {'bine'},'-i-e': {'jive'}}) function")
    if max_partition({'---x': {'onyx'}, '--x-': {'waxy'}, '----': {'wavy'}})!='----':
        print(f"Error with max_partition({'---x': {'onyx'}, '--x-': {'waxy'}, '----': {'wavy'}}) function")
    if max_partition({'w---': {'waxy', 'wavy'}, '----': {'onyx'}})!='w---':
        print(f"Error with max_partition({'w---': {'waxy', 'wavy'}, '----': {'onyx'}}) function")
    if max_partition({'i--': {'ivy'}})!='i--':
        print(f"Error with max_partition({'i--': {'ivy'}}) function")
    if max_partition({'----': {'alma', 'clio', 'novi'}, '--------': {'standish'}})!='----':
        print(f"Error with max_partition({'----': {'alma', 'clio', 'novi'}, '--------': {'standish'}}) function")
    if max_partition({'s---': {'sand'}, 'ti-e': {'tide'}, '-i--': {'rino'}})=='-i--' or 's---':
        pass
    else:
        print("Error with max_partition({'s---': {'sand'}, 'ti-e': {'tide'}, '-i--': {'rino'}}) function")


def clean_partition(partitions,key):
    """Returns the value corresponding to the key for the largest partitie set

    Args:
        partitions (dict): partitions from partition function
        key(str): key from max_partition function

    Returns:
        str: dictionary value of the maximum partite set

    """
    key=max_partition(partitions)
    #Iterating through all keys created from partition
    for i in list(partitions):
        #For all keys that aren't the max partite set, we will remove them from the dictionary
        if i!=key:
            del partitions[i]
            #We are left with only one key, which is the key for the largest partitie set. 
            #We will return value of this key

    return list(partitions.values())[0]


def test_clean_partition():
    """Tests the clean_partition function over 6 tests

    Args:
        None: We will call clean_partition function later

    Returns:
        String: We will get an error message indicating that something is wrong with the clean_partition function
    """
    if clean_partition({'i-y': {'ivy'}},'i-y')!={'ivy'}:
        print("Error with clean_partition({'i-y': {'ivy'}},'i-y') function")
    if clean_partition({'f---': {'frog'}, '----': {'damp', 'meat'}, '--i-': {'gain'}},'----')!={'damp', 'meat'}:
        print("Error with clean_partition({'f---': {'frog'}, '----': {'damp', 'meat'}, '--i-': {'gain'}},'----') function")
    if clean_partition({'-----e': {'muncie'}, '-e--e-': {'denver'}, '------': {'boston'}},'------')!={'boston'}:
        print("Error with clean_partition({'-----e': {'muncie'}, '-e--e-': {'denver'}, '------': {'boston'}},'------') function")
    if clean_partition({'---ivi-y': {'activity'}, '-----i-e': {'practice'}},'-----i-e')!={'practice'}:
        print("Error with clean_partition({'---ivi-y': {'activity'}, '-----i-e': {'practice'}},'-----i-e') function")
    if clean_partition({'----': {'rino'}, 't-de': {'tide'}, 's--d': {'sand'}},'----')!={'rino'}:
        print("Error with clean_partition({'----': {'rino'}, 't-de': {'tide'}, 's--d': {'sand'}},'----') function")
    if clean_partition({'-i--': {'rino'}, 's---': {'sand'}, 'ti-': {'tid'}},'s---')=={'rino'} or {'sand'}:
        pass
    else:
        print("Error with clean_partition({'-i--': {'rino'}, 's---': {'sand'}, 'ti-': {'tid'}},'s---') function")
    if clean_partition({'-i--': {'rino'}, 's---': {'sand'}, 'ti-': {'tid'}},'-i--')=={'rino'} or {'sand'}:
        pass
    else:
        print("Error with clean_partition({'-i--': {'rino'}, 's---': {'sand'}, 'ti-': {'tid'}},'-i--') function")


def read_input(guesses):
    """Allow user to enter in letters as a guess

    Args:
        guesses(str): User will be input to enter a letter

    Returns:
        guess(str): Returns  the guess of the user. 
    """
    while True:
        guess=input("Enter a letter: ").lower()

        if len(guess) !=1:
            print("Enter Only One Letter")
        elif not guess.isalpha():
            print("That isn't a letter, try again")
        elif guess in guesses:
            print("You've already guessed that")
        else:
            return guess


def read_int():
    """Allows the user to input the length of words they want to play with

    Args:
        None: We will input the user to enter a number that will act as our word length 

    Returns:
        length(int): Length of words that the user will play with. 
    """
    while True:
        try:
            length=int(input("Length?: "))
            return length 
        except:
            print("That is not a number!")


def testing():
    """Consolidates all testing functions

    Args:
        None: We will call testing functions later

    Returns:
        String: We will get an error message indicating that something is wrong with one of these functions
    """
    test_game_over()
    test_mask_word()
    test_partition()
    test_max_partition()
    test_clean_partition()


def main():
    """Plays a game of Hangman

    Args:
        None: We will utilize all functions to play hangman

    Returns:
        String: We will print out a statement that either declares the user a winner or a loser
    """
    #Game Setup
    length=read_int()
    cheat=length<0 
    length=abs(length)
    words=load_words("hangman_words.txt", length)
    if len(words)<1:
        print("No words found of that length")
        return 
    wordset=set(words)
    NumOfWords=len(wordset)
    NumGuesses=5
    guesses=set()
    WordsSeen=set()
    hint=str("-"*length) 


    #Game Loop
    while not game_over(NumGuesses,hint):
        if cheat:
            if NumGuesses==5:
                print(f"The potential words are {wordset}")
                print(f"There are {NumOfWords} possible words")
            else:
                print(f"The potential words are {NewWordSet}")
                print(f"There are {NWSLength} possible words")
        
        #Print Out game state
        print(f"You have {NumGuesses} guesses remaining")
        print(f"Guessed Letters: {guesses}")
        print(f"Current Hint: {hint}")
       
        #Get New Input
        guess=read_input(guesses)

        #Updated Game State
        guesses.add(guess)
        if NumGuesses==5:
            partitions=partition(wordset,guess)
            #Once we hit the last word in wordset, we want to apply all guesses so that it 
            #iterates and a partition is done on just that word
            if NumOfWords==1:
                partitions=partition(wordset,guesses)
        else:
            partitions=partition(NewWordSet,guesses)
        Selected_Partition=max_partition(partitions)
        result = '\n'.join(f'{key}: {value}' for key, value in partitions.items())
        if cheat:
            print(f"Partitons:\n{result}")
            print(f"Selected Partition: {Selected_Partition}")
        
        #This gives us wordset for the key of max partite set. We can use this wordset to 
        #Eliminate words that we've already seen and get it down to 1 word. 
        NewWordSet=clean_partition(partitions,Selected_Partition)
        NWSLength=len(NewWordSet)
        next_hint=Selected_Partition
        if hint!=next_hint:

            #Correct Guess
            print(f"Correct! {guess} is in the word!")
            NumGuesses=NumGuesses-1

            #Allows user to get correct guesses easier in cheat mode
            if cheat:
                NumGuesses=NumGuesses+1
        else:
            print(f"I'm sorry, {guess} is not in the word!")
            NumGuesses=NumGuesses-1
        hint=next_hint
        WL=list((NewWordSet))
        #Declaring our answer at the end
        answer=rnd.choice(WL)
    
    #Game End Conditions/Messages
    if hint.count("-")==0:
        print(f"You've won! The word was {answer}")
    else:
        print(f"You Lose! The word was {answer}")


if __name__=="__main__":
    testing()
    main()
