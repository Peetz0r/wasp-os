import manager, logo, gc

watch.display.fill(0)
watch.drawable.rleblit(logo.pine64, fg=0xffff)
watch.vibrator.pulse()
watch.drawable.rleblit(logo.pine64, fg=0x001f, slowdown=1000) # this takes ~2 seconds
gc.collect()

wasp = manager.Manager(watch)
wasp.run()
