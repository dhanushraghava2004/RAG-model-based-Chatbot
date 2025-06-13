create a .env file and past the following 


PINECONE_API_KEY=pcsk_PUWYG_2FZGYQuQHvYGSEhcJHMwfZevZjECYGV759Wr6Ts1QRjgMML9AK6Z1haDZZX4Lbj
HUGGINGFACE_API_KEY=hf _ FKtrRHlziKtQHWHBCQLIZodQaqClvVBfFR
OPENAI_API_KEY=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
MISTRAL_API_KEY=hxDcPrCPRCu01vWYtZ5XYUhkeD4CdM0i




then run the src/ python files 

then copy the json file from the workflows asn past it in n8n

then execute it with postman or  curl with 

http://localhost:5678/webhook-test/webhook as the trigger 


then you can see the output in logs/chatbot.log text file
