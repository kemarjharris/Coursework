#include <linux/module.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

MODULE_INFO(vermagic, VERMAGIC_STRING);

struct module __this_module
__attribute__((section(".gnu.linkonce.this_module"))) = {
 .name = KBUILD_MODNAME,
 .init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
 .exit = cleanup_module,
#endif
 .arch = MODULE_ARCH_INIT,
};

static const struct modversion_info ____versions[]
__used
__attribute__((section("__versions"))) = {
	{ 0x355992de, "module_layout" },
	{ 0x126bda94, "per_cpu__current_task" },
	{ 0xb72397d5, "printk" },
	{ 0xb8f3a590, "sys_call_table" },
	{ 0xb4390f9a, "mcount" },
	{ 0xc58cdb60, "lookup_address" },
};

static const char __module_depends[]
__used
__attribute__((section(".modinfo"))) =
"depends=";


MODULE_INFO(srcversion, "DFF888E59A86BCFCC1BC58B");
