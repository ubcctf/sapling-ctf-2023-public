If you are using MacOS, you need to install a *virtual machine* running a Linux operating system in order to easily run many challenges, particularly those in REV and PWN.\n

You can download a VM like [VirtualBox](https://www.virtualbox.org/). After downloading VirtualBox, you'll want to install a Linux distribution. Any Linux distribution is fine, and you can pick Ubuntu.\n

Ubuntu provides a step-by-step guide to setting up a Ubuntu VM in VirtualBox. You can find it [here](https://ubuntu.com/tutorials/how-to-run-ubuntu-desktop-on-a-virtual-machine-using-virtualbox).\n

It may be useful to have shared folders so you can move files quickly between your VM and your OS. A decent guide to that can be found [here](https://medium.com/macoclock/share-folder-between-macos-and-ubuntu-4ce84fb5c1ad).

Once you have set up your VM, download the file attached, open it up in the terminal *in your VM*, navigate to the directory you downloaded the file into, and run `./flag`. You should see your first flag!
  
You don't need to use a VirtualBox VM. There are other solutions, such as using a Docker container, using VMWare, or using a remote server. You can use repl.it to solve many challenges. It is also possible to solve many challenges using the CS student servers. 