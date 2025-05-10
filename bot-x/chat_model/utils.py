Chathistory = ()



def save_user_chat_history(bot_id, user_id, timestamp, user_message, bot_message, user_audio_message,bot_audio_message, sentiment):
   
    new_user_chat_history = Chathistory(
        bot_id=bot_id, 
        user_id=user_id,
        timestamp=timestamp,
        user_message=user_message,
        bot_message=bot_message,
        user_audio_message=user_audio_message,
        bot_audio_message=bot_audio_message,
        sentiment=sentiment
        )
    
    db.session.add(new_user_chat_history)
    db.session.commit()
    


def load_chat_history(bot_id):
    
    # Retrieve the chat history for the given bot_id
    chat_history_records = ChatHistory.query.filter_by(bot_id=bot_id).all()
    

    if chat_history_records:
        chat_history = []
        chat_hitory_for_model = []
        for record in chat_history_records:
            chat_hitory_for_model.append({
                "input": record.user_message,
                "output":record.bot_message
            })
            
            # Check for audio message
            if record.user_audio_message is None:
                chat_history.append({
                    "input":  {"type": "text", "content": record.user_message},
                    "output": {"type": "text", "content": record.bot_message}
                })
                
            else:
                chat_history.append({
                    "input":  {"type": "audio", "content": record.user_audio_message},
                    "output": {"type": "audio", "content": record.bot_audio_message}
                })
                    

                print(chat_history)
        return {"chat_history": chat_history}, chat_hitory_for_model
    else:
        return {"chat_history": []} , []
    


def get_bot_profile_data(bot_id, frame):
    
    bot = db.session.query(Profile).filter(Profile.id == bot_id).first()
    if not bot:
        return None

    name = bot.name
    role = bot.role
    file = bot.filename
    audio = bot.audiofile
    print(f'Name: {name}\nRelation: {role}\nFile: {file}\n')
    
    clean_text = remove_date_and_time(f'uploads/{file}')
    converted_format = convert_into_list_of_dictionary(clean_text)

    updated_frame, updated_sentiment, updated_emotion = perform_emotion_analysis_on_frame(frame)
    print('Sentiments and Emotions:', type(updated_sentiment), type(updated_emotion))
    
    if updated_sentiment != None and updated_emotion != None: 
        sentiment = updated_sentiment + "|" + updated_emotion
    else:
        sentiment = None
        
    config = {
        'name': name, 
        'relation': role,
        'converted_format': converted_format,
        'sentiment': updated_sentiment,
        'emotion': updated_emotion,
        'system_message': system_message,
    }
    return config, audio, sentiment