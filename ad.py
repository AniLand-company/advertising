import disnake
from disnake.ext import commands
from disnake import TextInputStyle

class AdModal(disnake.ui.Modal):
    def __init__(self, ad_type):
        self.ad_type = ad_type
        
        if ad_type == "rp":
            components = [
                disnake.ui.TextInput(
                    label="Ссылка на Discord сервер",
                    placeholder="https://discord.gg/...",
                    custom_id="discord_link",
                    style=TextInputStyle.short,
                    required=True,
                ),
                disnake.ui.TextInput(
                    label="Описание сервера",
                    placeholder="Топ-2 сервер по JuniperBot-у",
                    custom_id="description",
                    style=TextInputStyle.paragraph,
                    required=True,
                    max_length=1000,
                ),
                disnake.ui.TextInput(
                    label="Ссылка на картинку",
                    placeholder="https://...",
                    custom_id="image_url",
                    style=TextInputStyle.short,
                    required=False,
                ),
            ]
            title = "Создание объявления - Пиар"
        else:
            components = [
                disnake.ui.TextInput(
                    label="Описание услуги",
                    placeholder="Пишу ботов дискорд на Java, примеры и цена в лс",
                    custom_id="service_description",
                    style=TextInputStyle.paragraph,
                    required=True,
                    max_length=1000,
                ),
                disnake.ui.TextInput(
                    label="Оплата",
                    placeholder="В зависимости от работы",
                    custom_id="price",
                    style=TextInputStyle.short,
                    required=True,
                ),
                disnake.ui.TextInput(
                    label="Ссылка на картинку",
                    placeholder="https://...",
                    custom_id="image_url",
                    style=TextInputStyle.short,
                    required=False,
                ),
            ]
            title = "Создание объявления - Услуги"
            
        super().__init__(title=title, components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        await inter.response.send_message("Создаю объявление...", ephemeral=True)
        
        try:
            if self.ad_type == "rp":
                discord_link = inter.text_values["discord_link"]
                description = inter.text_values["description"]
                image_url = inter.text_values.get("image_url", "")
                
                if not image_url:
                    image_url = "https://i.ibb.co/Q70hP5PF/Untitled-47.png"
                
                embed = disnake.Embed(color=0x2b2d31)
                
                description = description[:1000] if len(description) > 1000 else description
                embed.add_field(name="Описание:", value=f"```{description}```", inline=False)
                
                embed.set_image(url=image_url)
                
                view = RPAdView(inter.author.id)
                
                discord_link = discord_link[:1950] if len(discord_link) > 1950 else discord_link
                await inter.channel.send(
                    content=discord_link,
                    embed=embed,
                    view=view
                )
                
                await inter.delete_original_message()
                
            else: 
                service_description = inter.text_values["service_description"]
                price = inter.text_values["price"]
                image_url = inter.text_values.get("image_url", "")
                
                if not image_url:
                    image_url = "https://i.ibb.co/Q70hP5PF/Untitled-47.png"
                
                embed = disnake.Embed(color=0x2b2d31)
                embed.title = "Мои услуги"
                
                service_description = service_description[:1000] if len(service_description) > 1000 else service_description
                embed.add_field(
                    name="🛒 Услуга:",
                    value=f"```{service_description}```",
                    inline=False
                )
                
                price = price[:100] if len(price) > 100 else price
                embed.add_field(
                    name="🛒 Оплата:",
                    value=f"```{price}```",
                    inline=False
                )
                
                embed.set_thumbnail(url=inter.author.display_avatar.url)
                
                embed.set_image(url=image_url)
                
                view = ServiceAdView(inter.author.id)
                
                await inter.channel.send(
                    content=f"{inter.author.mention}",
                    embed=embed,
                    view=view
                )
                
                await inter.delete_original_message()
                
        except disnake.errors.HTTPException as e:
            if "Must be 2000 or fewer in length" in str(e):
                await inter.edit_original_message(content="Ошибка: текст сообщения слишком длинный (превышен лимит Discord в 2000 символов). Пожалуйста, сократите описание.")
            else:
                await inter.edit_original_message(content=f"Произошла ошибка: {str(e)}")

class RPAdView(disnake.ui.View):
    def __init__(self, author_id: int):
        super().__init__(timeout=None)
        self.author_id = author_id
        
        create_btn = disnake.ui.Button(
            style=disnake.ButtonStyle.secondary,
            label="Создать пиар",
            emoji="🤝",
            custom_id=f"create_rp_post"
        )
        create_btn.callback = self.create_callback
        self.add_item(create_btn)
        
        delete_btn = disnake.ui.Button(
            style=disnake.ButtonStyle.secondary,
            emoji="🗑️",
            custom_id=f"delete_ad_rp_{author_id}"
        )
        delete_btn.callback = self.delete_callback
        self.add_item(delete_btn)
    
    async def create_callback(self, inter: disnake.MessageInteraction):
        modal = AdModal("rp")
        await inter.response.send_modal(modal)
    
    async def delete_callback(self, inter: disnake.MessageInteraction):
        if inter.author.id == self.author_id or inter.channel.permissions_for(inter.author).manage_messages:
            await inter.message.delete()
            await inter.response.send_message("Объявление удалено!", ephemeral=True)
        else:
            await inter.response.send_message("У вас нет прав для удаления этого объявления!", ephemeral=True)

class ServiceAdView(disnake.ui.View):
    def __init__(self, author_id: int):
        super().__init__(timeout=None)
        self.author_id = author_id
        
        dm_btn = disnake.ui.Button(
            style=disnake.ButtonStyle.link,
            label="Написать автору",
            emoji="✉️",
            url=f"https://discord.com/users/{author_id}"
        )
        self.add_item(dm_btn)
        
        create_btn = disnake.ui.Button(
            style=disnake.ButtonStyle.secondary,
            label="Создать свой пост",
            emoji="✏️",
            custom_id=f"create_service_post"
        )
        create_btn.callback = self.create_post_callback
        self.add_item(create_btn)
        
        delete_btn = disnake.ui.Button(
            style=disnake.ButtonStyle.secondary,
            emoji="🗑️",
            custom_id=f"delete_ad_service_{author_id}"
        )
        delete_btn.callback = self.delete_callback
        self.add_item(delete_btn)
    
    async def create_post_callback(self, inter: disnake.MessageInteraction):
        modal = AdModal("services")
        await inter.response.send_modal(modal)
    
    async def delete_callback(self, inter: disnake.MessageInteraction):
        if inter.author.id == self.author_id or inter.channel.permissions_for(inter.author).manage_messages:
            await inter.message.delete()
            await inter.response.send_message("Объявление удалено!", ephemeral=True)
        else:
            await inter.response.send_message("У вас нет прав для удаления этого объявления!", ephemeral=True)

class CreateButton(disnake.ui.Button):
    def __init__(self, ad_type):
        super().__init__(
            style=disnake.ButtonStyle.success,
            label="Создать",
            custom_id=f"create_ad_{ad_type}"
        )
        self.ad_type = ad_type

    async def callback(self, inter: disnake.MessageInteraction):
        modal = AdModal(self.ad_type)
        await inter.response.send_modal(modal)

class InitialView(disnake.ui.View):
    def __init__(self, ad_type):
        super().__init__(timeout=300)
        self.add_item(CreateButton(ad_type))

class AdCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(RPAdView(0))
        self.bot.add_view(ServiceAdView(0))

    @commands.slash_command(name="ad", description="Создать объявление")
    @commands.has_permissions(administrator=True)
    async def ad(self, inter: disnake.ApplicationCommandInteraction):
        pass

    @ad.sub_command(name="rp", description="Создать объявление для пиара сервера")
    async def ad_rp(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title="📢 Создание объявления - Пиар",
            description="Нажмите на кнопку ниже, чтобы создать объявление для пиара вашего Discord сервера.",
            color=0x2F3136
        )
        view = InitialView("rp")
        await inter.response.send_message(embed=embed, view=view, ephemeral=True)

    @ad.sub_command(name="services", description="Создать объявление об услугах")
    async def ad_services(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title="💼 Создание объявления - Услуги",
            description="Нажмите на кнопку ниже, чтобы создать объявление о ваших услугах.",
            color=0x2F3136
        )
        view = InitialView("services")
        await inter.response.send_message(embed=embed, view=view, ephemeral=True)

def setup(bot):
    bot.add_cog(AdCog(bot))
print("""
################################################################################
#                                                                              #
#                                  ######      ######                          #
#                                 #      #    #      #                         #
#                                 #      #    #      #                         #
#                                 #######     #######                          #
#                                 #      #    #      #                         #
#                                 #      #    #      #                         #
#                                 #      #    #######                          #
#                                                                              #
#                               Автор: EndermanHack19                          #
#                                                                              #
#    Ресурсы:                                                                  #
#    GitHub EndermanHack19:  https://github.com/EndermanHack19                 #
#    GitHub AniLand-company:  https://github.com/AniLand-company               #
#    Discord:                https://discord.gg/Kmpk7sBCVQ                     #
#                                                                              #
################################################################################
""")
