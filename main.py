from time import sleep, perf_counter
from without_image.whatsApp import WhatsApp

with WhatsApp() as bot:

    data = bot.get_recipients('', "")
    data['received'] = False
    bot.land_on_whatsapp()
    sleep(15)
    limit = 50
    offset = 0
    while True:
        for index, row in data[offset:limit+offset].iterrows():
            tic = perf_counter()
            try:
                print('here')
                bot.send_message(row['phone'], row['message'])
            except Exception:
                data[:index+1].to_csv('Test_sended.csv', index=False)
            else:
                data.at[index, 'received'] = True
        offset += limit
        sleep(300)
        if index+1 % data.shape[0]==0:
            toc = perf_counter()
            break
    
toc = perf_counter()
print(f"pricing_data/Jumia's simulation ended after {toc - tic:0.4f} seconds")
