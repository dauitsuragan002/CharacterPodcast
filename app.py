import datetime
import logging

from config import CHAR_ID, char_token, client, get_message

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("podcast")

async def create_podcast(char1_name, char2_name, initial_topic, num_exchanges=5, lang="en"):
    """
    Create a podcast-like conversation between two characters.
    
    Args:
        char1_name: Name of the first character from CHAR_ID
        char2_name: Name of the second character from CHAR_ID
        initial_topic: The initial topic or question to start the conversation
        num_exchanges: Number of back-and-forth exchanges between characters
        lang: Language code for localization
    
    Returns:
        A list of dictionaries with the conversation history
    """
    session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    logger.info(get_message("podcast_start", lang, char1_name, char2_name) if "podcast_start" in globals().get("MESSAGES", {}) else f"Starting podcast between {char1_name} and {char2_name}")
    
    await client.authenticate(char_token)
    
    if char1_name not in CHAR_ID or char2_name not in CHAR_ID:
        error_msg = get_message("char_not_found", lang) if "char_not_found" in globals().get("MESSAGES", {}) else "One or both characters not found in CHAR_ID dictionary"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    character_id1 = CHAR_ID[char1_name]
    character_id2 = CHAR_ID[char2_name]
    
    logger.info(f"Creating chat for {char1_name}")
    
    chat1, greeting_message = await client.chat.create_chat(character_id1)
    chat2, greeting_message = await client.chat.create_chat(character_id2)
    
    logger.info(f"Creating chat for {char2_name}")
    
    conversation = [
        {"speaker": "Host", "message": initial_topic}
    ]
    
    logger.info(f"Sending initial topic to {char1_name}")
    response1 = await client.chat.send_message(character_id1, chat1.chat_id, initial_topic)
    char1_response = response1.get_primary_candidate().text
    conversation.append({"speaker": char1_name, "message": char1_response})
    
    current_message = char1_response
    
    for i in range(num_exchanges):
        logger.info(f"Exchange {i+1}/{num_exchanges}")
        
        logger.info(f"Waiting for {char2_name}'s response")
        response2 = await client.chat.send_message(character_id2, chat2.chat_id, current_message)
        char2_response = response2.get_primary_candidate().text
        conversation.append({"speaker": char2_name, "message": char2_response})
        
        logger.info(f"Waiting for {char1_name}'s response")
        response1 = await client.chat.send_message(character_id1, chat1.chat_id, char2_response)
        char1_response = response1.get_primary_candidate().text
        conversation.append({"speaker": char1_name, "message": char1_response})
        
        current_message = char1_response
    
    logger.info(get_message("podcast_completed", lang, len(conversation)) if "podcast_completed" in globals().get("MESSAGES", {}) else f"Podcast completed with {len(conversation)} messages")
    
    return conversation, session_id
