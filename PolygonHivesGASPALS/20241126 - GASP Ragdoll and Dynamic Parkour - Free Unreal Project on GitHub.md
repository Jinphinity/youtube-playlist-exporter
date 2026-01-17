# GASP Ragdoll and Dynamic Parkour - Free Unreal Project on GitHub (20241126)

hello everyone and welcome to another gasp ALS project update so in this video I'm going to show you some of the plan features that were implemented and also we're going to discuss towards the end of the video some of the upcoming features so the first feature that was implemented is dynamic traversal so now any geometry that is blocking the traversible Collision channel is traversible and any geometry that is not blocking this channel is not reversible also there's a limit to the rotation

angle so this ones for example are not reversible but these ones they're working just fine um this is courtesy of Mr tapa on Twitter that uh made this and also showed uh on a x tread or Twitter tread how to do it so here we have this component that is doing Dynamic tracing we can activate the debug and we can see how this works so I will link the uh Twitter X tread in the description if you guys

want to understand how this is done it's a very very cool tread uh for this system but also for understanding traversal uh and parkour as a whole so there are still some limitations sometimes but overall it's working really fine and the previous blocks were also working of course because this is basically not uh different from what we had before it's just that it's doing the tracing dynamic Tech Al it doesn't matter what geometry we're in so the

second feature that we're going to discuss H is one of the most requested features and that is ragd doll so we have ragd dolls now in the game and they are implemented properly meaning that the Get Up animations from ALS are also implemented depending on if we fall down like uh on our belly or on our back it's also working in all the weird conditions I

made sure that they are like always behaving correctly so there were a lot of tutorials on how to implement ragd doll for gasp but if you just activate ragd doll um basically your capsule stays in place but then your meshes is going to some other place and when you recover from it you will basically teleport so ALS was doing this really well basically by moving the capsule and the actor uh

on tick when you're in a raged all position so I've taken everything from ALS and put it back with some tweaks so it's uh really cool working fine and it gives a nice rag doll effect to the game it's also working if you're crouched or not so if you're crouched and you go to rag doll and then you get up up it's you're still in Crouch and if you're standing up and going to R doll well you're still

standing up uh on the road to get in here like I had some really really weird bugs that I will put on the video so just for the fun [Music]

also one quick note is the Regal is replicated so the way the ragdo is replicated uh as some of you may know like it's pretty complicated to replicate um rag dolls because replicating physics is uh not an easy thing in unreal the way the rag doll is replicated is basically uh once the r doll is triggered it is plain on both the client and the server

uh so it can look different from client in server but then when you recover from the rll like it's using the client position so that the you don't teleport so this could be a bit cheat uh but it is working fine so as you see here uh I'm teleported um to where the uh the position of the owning client was and this is how um I replicated the rag doll but it is

working and it is replicated with the uh Get Up animations and all of that there were uh some uh issues with the transitions for example when we were going to crouch and standing up with the overlays there were some snapping but those were fixed as well and there were some issues when like after after the uh traversal montages the hand I was acting a bit finicky that's also

fixed all right so as for the upcoming features so I'm still trying to find a proper way to do um item attachments and to have everything work fine with uh all kinds of meeses so this is something that I didn't figure out yet trying to find like a proper position I know that a lot of you guys also asked for um a tutorial on how to do for example sword with with

attack animations I'm going to get to that but in order to get to that I want to fix this um issue the attachment issue and the hand offsets so that the tutorial is actually up to date with everything in the upcoming updates I will find a way uh to attach items properly and also I will be making a tutorial on how to do a sword with animations that's not going to be very complicated to do and after that we're going to see where we go from there

probably some more um traversal animations some more traversal actions um and some some other goodies as we go forward uh I also want to work a little bit on the camera so um there is a uh um a person on YouTube that contacted me and sent sent me a more Dynamic camera with basically shoulder switching I will Implement that and I want to do also first person so we'll have first person and we'll have a more

complete third person camera I hope you guys like these updates uh don't forget to like And subscribe um don't forget to share these with your friends so I've been working on this for quite some time now um if you want to collaborate if you want to participate to the project you can do p ests on on GitHub so yeah that's it for this update uh if you guys have any questions don't hesitate to post them in the comment as always I try to answer each and every single comment um if you

have any requests you can send them I don't promise anything but I will try to do my best and uh as always thank you guys for watching please like And subscribe and see you guys in the next video
