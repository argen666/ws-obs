while true; do
                ffmpeg...
                retval="$?"
                if [ "$retval" == "15" ]; then
                        break
                elif [ "$retval" == "16" ]; then
                        break
                elif [ "$retval" == "17" ]; then
                        break
				elif [ "$retval" == "20" ]; then
						sudo /sbin/reboot
                else
                        sleep 20
                fi
done
