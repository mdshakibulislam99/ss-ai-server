<?php
/**
 * Authentication handler for API requests.
 *
 * @package SS_AI_Image_Search
 * @subpackage Api
 */

declare( strict_types=1 );

namespace SS_AI_Image_Search\Api;

use SS_AI_Image_Search\Exceptions\Api\AuthenticationException;

/**
 * Authentication class for handling API key authentication.
 */
class Authentication {

	/**
	 * API key value.
	 *
	 * @var string
	 */
	private string $api_key;

	/**
	 * Authentication header name.
	 *
	 * @var string
	 */
	private string $header_name;

	/**
	 * Constructor.
	 *
	 * @param string $api_key API key for authentication.
	 * @param string $header_name Optional custom header name. Default 'X-API-Key'.
	 */
	public function __construct( string $api_key, string $header_name = 'X-API-Key' ) {
		$this->api_key     = $api_key;
		$this->header_name = $header_name;
	}

	/**
	 * Get authentication headers.
	 *
	 * @return array<string, string> Headers array.
	 */
	public function get_headers(): array {
		return array(
			$this->header_name => $this->api_key,
		);
	}

	/**
	 * Validate API key.
	 *
	 * @param string $api_key API key to validate.
	 * @return bool True if valid, false otherwise.
	 */
	public function validate( string $api_key ): bool {
		return hash_equals( $this->api_key, $api_key );
	}

	/**
	 * Get the API key.
	 *
	 * @return string API key.
	 */
	public function get_api_key(): string {
		return $this->api_key;
	}

	/**
	 * Set the API key.
	 *
	 * @param string $api_key API key to set.
	 * @return void
	 */
	public function set_api_key( string $api_key ): void {
		$this->api_key = $api_key;
	}

	/**
	 * Get the header name.
	 *
	 * @return string Header name.
	 */
	public function get_header_name(): string {
		return $this->header_name;
	}

	/**
	 * Set the header name.
	 *
	 * @param string $header_name Header name to set.
	 * @return void
	 */
	public function set_header_name( string $header_name ): void {
		$this->header_name = $header_name;
	}
}