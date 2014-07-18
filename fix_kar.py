#!/usr/bin/python

import subprocess, tempfile, shutil, sys, os, os.path

unzip = "C:/Program Files/7-Zip/7z"
unzipcmd = "x"
jar = "c:/Program Files/Java/jdk1.6.0_45/bin/jar"
copy = "copy"
zipper = "C:/Program Files/7-Zip/7z"

unwanted_libs = ["activation", "asm-", "geronimo-jaxws", "javax.ws.rs-api-",
"jaxb-impl-", "jaxb-xjc-", "jaxp-api", "jaxp-ri", "mail", "serializer-", "stax2-api-",
"velocity-", "woodstox-core-", "xalan-"]

tmpdir = tempfile.mkdtemp()
karfile = sys.argv[1]

def fix_libs():
	result = False
	for root, dirs, filenames in os.walk("lib"):
		for f in filenames:
			for lib in unwanted_libs:
				if f.count(lib) > 0:
					print "\tremoving", os.path.join(root, f)
					os.remove(os.path.join(root, f))
					result = True
					continue
	return result

def fix_manifest(fl):
	header = []
	classpath = ["Bundle-ClassPath: ."]
	tail = []
	i = 0

	with open(fl, "r+") as mf:
		lines = mf.readlines()

		for l in lines: #collecting header
			if not l.startswith("Bundle-ClassPath: "):
				header.append(l)
				i = i+1
			else:
				break

		for l in lines[i:]: #skipping Bundle-ClassPath
			if l.startswith(" ") or l.startswith("Bundle-ClassPath: "):
				i = i +1
			else:
				break

		for l in lines[i:]: #collecting tail
			tail.append(l)

	for root, dirs, filenames in os.walk("lib"):
		for f in filenames:
			classpath.append(",\n " + "lib/" + f)

	with open(fl, "w") as mf:
		mf.writelines(header)
		mf.writelines(classpath)
		mf.write("\n")
		mf.writelines(tail)

def pack_jar(fl, manifest):
	fldr="."
	pl = subprocess.Popen([jar, "cvfm", fl, manifest, "-C", fldr, "."], stdout=subprocess.PIPE)
	pl.communicate()

def unpack_file(fl):
	pl = subprocess.Popen([unzip, unzipcmd, fl], stdout=subprocess.PIPE)
	pl.communicate()

def fix_jar(folder, fl):
	print "Processing", fl
	olddir = os.getcwd()

	try:
		os.chdir(folder)
		unpack_file(fl)
		
		if fix_libs():
			os.remove(fl)
			tmpdir2 = tempfile.mkdtemp()
			shutil.copy("META-INF/MANIFEST.MF", tmpdir2)
			#os.remove("META-INF/MANIFEST.MF")
			shutil.rmtree("META-INF")
			tmpmf = tmpdir2+"/MANIFEST.MF"
			fix_manifest(tmpmf)
			pack_jar(fl, tmpmf)
			shutil.rmtree(tmpdir2)

		for root, dirs, filenames in os.walk("."):
			for d in dirs:
				#print "\twill rmtree", os.path.join(root,d)
				shutil.rmtree(os.path.join(root,d))
			for f in filenames:
				if not f == fl:
					#print "\twill delete file", os.path.join(root,f)
					os.remove(os.path.join(root,f))

	finally:
		os.chdir(olddir)

def unpack_kar(fl):
	oldpath = os.getcwd()
	try:
		shutil.copy(fl, tmpdir)
		os.chdir(tmpdir)
		unpack_file(fl)
		os.remove(fl)
	except (WindowsError, OSError), e:
		raise e
	finally:
		os.chdir(oldpath)

try:
	unpack_kar(karfile)
	for root, dirs, filenames in os.walk(tmpdir):
	    for f in filenames:
	        if f.endswith(".jar") and f.count("-bundle-") == 0:
	        	fix_jar(root, f)

	pl = subprocess.Popen([zipper, "a", "-tzip", karfile+".tmp", tmpdir+"/repository"], stdout=subprocess.PIPE)
	pl.communicate()
	os.remove(karfile)
	os.rename(karfile+".tmp", karfile)

finally:
	shutil.rmtree(tmpdir)
