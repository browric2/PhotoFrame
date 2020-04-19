import Settings
screen = Settings.screen
tframes = Settings.tframes


def fade(player):
    delta_alph = int(255 / tframes)
    if player.alph >= 0:

        player.picfit.set_alpha(player.alph)
        screen.fill(player.home_colour)
        screen.blit(player.picfit2, (0, 0))
        screen.blit(player.picfit, player.where)
        player.alph -= delta_alph

    else:
        where = (0, 0)
        player.picfit.set_alpha(0)
        screen.fill(player.home_colour)
        screen.blit(player.picfit2, where)

        player.picfit = player.picfit2
        player.mode = 'start'
        player.alph = 255
        player.startcount, player.shifted, player.endcount = 0, 0, 0
