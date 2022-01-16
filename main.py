from src.model.StyleTransfer import StyleTransfer

if __name__ == '__main__':

    style_path = 'style2.jpg'
    content_path = 'cat.jpg'

    s_transfer = StyleTransfer(style_path, content_path)
    s_transfer.run_style_transfer(num_steps=100)
    s_transfer.save_image('new.jpg')
    s_transfer.to_pil()