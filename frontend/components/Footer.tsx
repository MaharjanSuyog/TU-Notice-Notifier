export default function Footer() {
	return (
		<footer className="relative h-44 w-full shrink-0 overflow-hidden sm:h-48 md:h-45">
			<div className="absolute bottom-0 left-1/2 w-full -translate-x-1/2 translate-y-[14%] text-center sm:w-auto sm:whitespace-nowrap md:translate-y-[22%]">
				<div
					className="
						select-none font-sans font-extrabold
						leading-[0.82] tracking-tight text-[#18231F]
						
						text-[clamp(100px,13vw,200px)] sm:leading-none sm:tracking-normal
						mask-[linear-gradient(to_bottom,transparent_0%,black_60%)]
						[-webkit-mask-image:linear-gradient(to_bottom,transparent_0%,black_60%)]
					">
					<span className="block sm:inline">IOST</span>
					<span className="block sm:inline sm:ml-[0.25em]">NOTICE</span>
				</div>
			</div>
		</footer>
	);
}
